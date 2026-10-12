"""Fast limits/routing tests; do not load librosa or run pitch analysis."""
import ast
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import Mock, patch
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
decoder = types.ModuleType('librosa')
decoder.load = Mock()
with patch.dict(sys.modules, {'librosa': decoder}):
    spec = importlib.util.spec_from_file_location('bounded_features', ROOT / 'height_guesser/feature_extractor.py')
    features = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(features)


class LimitsTests(unittest.TestCase):
    def setUp(self):
        decoder.load.reset_mock()
        self.temp = tempfile.TemporaryDirectory()
        self.audio = Path(self.temp.name) / 'clip.webm'
        self.audio.write_bytes(b'fixture')

    def tearDown(self):
        self.temp.cleanup()

    def test_decoder_is_bounded_before_analysis(self):
        decoder.load.return_value = (np.ones(16000), 16000)
        y, rate = features.load_bounded_audio(self.audio)
        self.assertEqual(rate, 16000)
        self.assertEqual(len(y), 16000)
        decoder.load.assert_called_once_with(self.audio, sr=16000, mono=True, duration=10)

    def test_oversized_upload_never_reaches_decoder(self):
        with self.audio.open('wb') as handle:
            handle.truncate(features.MAX_AUDIO_BYTES + 1)
        with self.assertRaises(ValueError):
            features.load_bounded_audio(self.audio)
        decoder.load.assert_not_called()

    def test_invalid_decoder_outputs_rejected(self):
        for y, rate in [(np.ones(160001), 16000), (np.ones(100), 96000),
                        (np.ones((100, 2)), 16000), (np.array([]), 16000),
                        (np.array([np.nan]), 16000)]:
            decoder.load.return_value = (y, rate)
            with self.subTest(shape=y.shape, rate=rate), self.assertRaises(ValueError):
                features.load_bounded_audio(self.audio)

    def test_api_rejects_oversized_file_and_cleans_it_without_analysis(self):
        # Execute the actual endpoint with lightweight boundary doubles.
        source = ast.parse((ROOT / 'height_guesser/app.py').read_text())
        endpoint = next(n for n in source.body if isinstance(n, ast.FunctionDef) and n.name == 'predict_height')
        endpoint.decorator_list = []
        module = ast.Module(body=[endpoint], type_ignores=[])
        upload = types.SimpleNamespace(filename='clip.wav', save=lambda path: Path(path).write_bytes(b'x' * (features.MAX_AUDIO_BYTES + 1)))
        extractor = Mock()
        namespace = dict(request=types.SimpleNamespace(files={'audio': upload}, form={}),
                         app=types.SimpleNamespace(config={'UPLOAD_FOLDER': self.temp.name}),
                         allowed_file=lambda name: True, secure_filename=lambda name: name,
                         uuid=types.SimpleNamespace(uuid4=lambda: 'fixture'), os=__import__('os'),
                         jsonify=lambda value: value, MAX_AUDIO_BYTES=features.MAX_AUDIO_BYTES,
                         extract_features=extractor)
        exec(compile(module, '<endpoint>', 'exec'), namespace)
        result, status = namespace['predict_height']()
        self.assertEqual(status, 413)
        self.assertIn('4 MiB', result['error'])
        extractor.assert_not_called()
        self.assertFalse((Path(self.temp.name) / 'fixture.wav').exists())

    def test_static_page_and_prediction_have_separate_routes(self):
        config = json.loads((ROOT / 'vercel.json').read_text())
        self.assertEqual(config['routes'][0], {'src': '/', 'dest': '/public/index.html'})
        self.assertEqual(config['routes'][1], {'handle': 'filesystem'})
        self.assertEqual(config['routes'][2]['src'], '/predict')
        self.assertEqual(config['routes'][2]['methods'], ['POST'])
        self.assertFalse(any(r.get('src') == '/(.*)' for r in config['routes']))
        self.assertEqual((ROOT / 'public/index.html').read_text(),
                         (ROOT / 'height_guesser/templates/index.html').read_text())


if __name__ == '__main__':
    unittest.main()
