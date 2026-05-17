import sys
import types

# minimal stubs so surgeon imports without external deps
fitz_stub = types.SimpleNamespace(csRGB=None, Page=object)
sys.modules.setdefault("fitz", fitz_stub)

class DummyImageObj:
    def __init__(self, w, h):
        self.width = w
        self.height = h
    @property
    def size(self):
        return (self.width, self.height)
    def rotate(self, *args, **kwargs):
        return self
    def thumbnail(self, size):
        mw, mh = size
        scale = min(mw / self.width, mh / self.height)
        self.width = int(self.width * scale)
        self.height = int(self.height * scale)
    def convert(self, _):
        class G:
            def histogram(self):
                h = [0] * 256
                h[255] = 0
                return h
        return G()

class PILImageStub:
    @staticmethod
    def frombytes(mode, size, samples):
        return DummyImageObj(size[0], size[1])

PIL_stub = types.SimpleNamespace(Image=PILImageStub)
sys.modules.setdefault("PIL", PIL_stub)
sys.modules.setdefault("PIL.Image", PILImageStub)

import surgeon  # noqa: E402


def test_default_repair_batch_policy_values():
    assert surgeon.default_repair_batch(8) == 1
    assert surgeon.default_repair_batch(16) == 2
    assert surgeon.default_repair_batch(24) == 4
    assert surgeon.default_repair_batch(40) == 8
    assert surgeon.default_repair_batch(48) == 8


def test_render_page_a6000_max_dim_preserved():
    class DummyPage:
        rotation = 0
        rect = types.SimpleNamespace(width=3000, height=2000)
        def get_pixmap(self, dpi, colorspace=None):
            return types.SimpleNamespace(width=3000, height=2000, samples=(b'\x00' * (3000 * 2000 * 3)))

    img, _ = surgeon.render_page(DummyPage(), dpi=72, min_crop_size=96, gpu_profile="a6000")
    assert img is not None
    assert max(img.width, img.height) == 1536


def test_render_page_default_max_dim_1280():
    class DummyPage:
        rotation = 0
        rect = types.SimpleNamespace(width=3000, height=2000)
        def get_pixmap(self, dpi, colorspace=None):
            return types.SimpleNamespace(width=3000, height=2000, samples=(b'\x00' * (3000 * 2000 * 3)))

    img, _ = surgeon.render_page(DummyPage(), dpi=72, min_crop_size=96, gpu_profile="default")
    assert img is not None
    assert max(img.width, img.height) == 1280


def test_repair_batch_env_override_wins(monkeypatch):
    monkeypatch.setenv("REPAIR_BATCH", "11")
    cfg = surgeon.SurgeonConfig.from_env(gpu_profile="default")
    assert cfg.repair_batch == 11


def test_repair_batch_default_without_gpu(monkeypatch):
    monkeypatch.delenv("REPAIR_BATCH", raising=False)
    cfg = surgeon.SurgeonConfig.from_env(gpu_profile="default")
    assert cfg.repair_batch == 1
