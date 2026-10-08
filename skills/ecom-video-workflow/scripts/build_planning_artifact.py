from pathlib import Path
import runpy
runpy.run_path(Path(__file__).with_name('analyze_video_evidence.py'), run_name='__main__')
