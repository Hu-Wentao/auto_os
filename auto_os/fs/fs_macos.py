import os
import shutil


def deep_copy(src: str, dst: str, show_log=False, reset_dst=True):
    """复制文件夹及内容
    注意,同时也复制符号链接, 而不是复制指向的文件, 适用于container存档覆盖场景
    :param src: 源
    :param dst: 目标
    :param show_log: 打印日志
    :param reset_dst: True 如果dst已经存在,则清空内容
    :return:
    """
    if show_log:
        print(f"deep_copy [{src} -> {dst}]")
    if os.path.exists(dst) and reset_dst:  # 已存在则清空内容
        shutil.rmtree(dst)

    if not os.path.exists(dst):  # 确保folder存在
        os.makedirs(dst)
    for item in os.listdir(src):
        src_item = os.path.join(src, item)
        dst_item = os.path.join(dst, item)

        if os.path.islink(src_item):
            link_target = os.readlink(src_item)
            os.symlink(link_target, dst_item)
        elif os.path.isdir(src_item):
            deep_copy(src_item, dst_item)
        else:
            shutil.copy2(src_item, dst_item)


def reset_folder(folder: str):  # rmtree 可能报错 xx路径不存在
    print(f"reset folder [{folder}]")
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)


def resource_path(file, res_path: str):
    """
    获取相对 .py文件的路径, 用于读取资源文件
    :param file: 固定传入对应.py的 __file__ 动态变量, 代表正在执行的.py文件的位置.(不一定是入口main.py的位置)
    :param res_path: 不带 ./ 或 / 的相对.py文件的路径
    :return:
    """
    current_path = os.path.dirname(os.path.abspath(file))
    # 获取图片的路径
    path = os.path.join(current_path, res_path)
    return path
