import os
import random
from setting import settings

def random_start_terms():
    start_dir = settings.START_TERNS_DIR
    file_name_list = os.listdir(start_dir)
    file_name = random.sample(file_name_list,1)[0]
    start_term_path = os.path.join(start_dir,file_name)
    return start_term_path

if __name__ == '__main__':
    random_start_terms()