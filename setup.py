import subprocess
import sys


req=['requests','logging','xml.etree.ElementTree','zipfile','pandas','boto3']

for i in req:
        try:
            __import__(i)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", i])
        finally:
            __import__(i)