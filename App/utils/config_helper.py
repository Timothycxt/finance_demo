import yaml
import os


def get_config_map():
    # 获取当前脚本所在文件夹路径
    # 获取yaml文件路径
    project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    yamlPath = os.path.join(project_path, 'config.yaml')
    # open方法打开直接读出来
    f = open(yamlPath, 'r', encoding='utf-8')
    cfg = f.read()
    res = yaml.load(cfg, Loader=yaml.FullLoader)  # 用load方法转字典
    return res

