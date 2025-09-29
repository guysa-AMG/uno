import os

def check_requirements():
    try:
        import pygame
        import pytest
    except ModuleNotFoundError:
        os.system("python3 -m pip install -r requirements.txt")
    
