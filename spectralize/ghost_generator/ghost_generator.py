import random
from dataclasses import dataclass
from glob import glob
from io import BytesIO
from pathlib import Path
from typing import Optional

import yaml
from PIL import Image, ImageOps

IMAGE_DIR = Path(__file__).parent / "images"


@dataclass
class Feature:
    path: str
    x: int
    y: int
    x2: Optional[int] = None
    y2: Optional[int] = None
    mirror: Optional[bool] = True
    chance: Optional[float] = 1

    @classmethod
    def from_dict(cls, d: dict, path):
        x2 = d.get("x2")
        y2 = d.get("y2")

        mirror = d.get("mirror", True)

        chance = d.get("chance", 1)

        if x2 is not None or y2 is not None:
            assert x2 is not None and y2 is not None

        return cls(
            path=path / d["path"],
            x=d["x"],
            y=d["y"],
            x2=x2,
            y2=y2,
            mirror=mirror,
            chance=chance,
        )

    def load(self) -> Image:
        return Image.open(self.path)


class GhostGenerator:
    def __init__(self):
        self.base = Image.open(IMAGE_DIR / "base.png")
        self.features = {}
        self.discover_features()

    def discover_features(self):
        for feature_config_file in glob(f"{str(IMAGE_DIR)}/*/config.yml"):
            with open(feature_config_file, "r") as f:
                feature_config = yaml.safe_load(f)

            feature_path = Path(feature_config_file).parent

            self.load_features(feature_config, feature_path)

    def load_features(self, feature_config, feature_path):
        feature_name = feature_config["name"]

        self.features[feature_name] = []

        for feature in feature_config["features"]:
            feature["chance"] = feature_config.get("chance", 1)
            self.features[feature_name].append(Feature.from_dict(feature, feature_path))

    def generate(self, **kwargs) -> Image:
        ghost = self.base.copy()

        random.seed(kwargs.get("seed"))

        for feature_type in self.features:
            if feature_type in kwargs:
                feature = self.features[feature_type][int(kwargs[feature_type]) - 1]
            else:
                feature = random.choice(self.features[feature_type])

                if random.random() > feature.chance:
                    continue

            loaded_feature = feature.load()

            ghost.paste(loaded_feature, (feature.x, feature.y), loaded_feature)

            if feature.x2 is not None:
                if feature.mirror:
                    mirrored = ImageOps.mirror(loaded_feature)
                else:
                    mirrored = loaded_feature

                ghost.paste(mirrored, (feature.x2, feature.y2), mirrored)

        return ghost

    def generate_bytes(self, **kwargs) -> BytesIO:
        ghost = self.generate(**kwargs)

        ghost_bytes = BytesIO()

        ghost.save(ghost_bytes, "png")
        ghost_bytes.seek(0)

        return ghost_bytes
