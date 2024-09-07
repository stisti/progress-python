import pytest
import time
from unittest.mock import patch, MagicMock
from progress.progress import ByteCounter, print_stats

@pytest.fixture
def counter():
    return ByteCounter()

def test_increment(counter):
    counter.increment(100)
    assert counter.byte_count == 100

def test_get_stats_initial(counter):
    byte_count, elapsed_time, speed = counter.get_stats()
    assert byte_count == 0
    assert elapsed_time == 0
    assert speed == 0

def test_get_stats_after_increment(counter):
    counter.increment(1000)
    time.sleep(0.1)  # Sleep to ensure some time has passed
    byte_count, elapsed_time, speed = counter.get_stats()
    assert byte_count == 1000
    assert elapsed_time > 0
    assert speed > 0

@pytest.mark.parametrize("bytes,time,speed", [
    (1000, 2.5, 400),
    (5000, 5.0, 1000),
    (0, 1.0, 0),
])
def test_print_stats(bytes, time, speed, capsys):
    counter = MagicMock()
    counter.get_stats.return_value = (bytes, time, speed)
    
    with patch('time.sleep', return_value=None), patch('progress.progress.STOPPING', [False, True]):
        print_stats(counter)
    
    captured = capsys.readouterr()
    assert f"Bytes: {bytes}" in captured.err
    assert f"Time: {time:.2f}s" in captured.err
    assert f"Speed: {speed:.2f} B/s" in captured.err

def test_print_stats_keyboard_interrupt(capsys):
    counter = MagicMock()
    counter.get_stats.return_value = (1000, 2.5, 400)
    
    with patch('time.sleep', side_effect=KeyboardInterrupt):
        print_stats(counter)
    
    captured = capsys.readouterr()
    assert captured.err == ""  # Ensure nothing is printed when interrupted