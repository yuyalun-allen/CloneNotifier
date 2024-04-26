import git
import shutil
import csv
import os

def extract_previous_version(repo_path, working_dir):
    # 打开 git 仓库
    repo = git.Repo(repo_path)
    
    # 获取当前分支
    current_branch = repo.active_branch
    
    # 获取上一个版本的 commit
    previous_commit = repo.commit(current_branch.name + "^")
    
    # 创建一个新目录来存储上一个版本的文件
    old_dir = os.path.join(working_dir, "old")
    os.makedirs(old_dir, exist_ok=True)
    
    # 将上一个版本的文件复制到新目录中
    for item in previous_commit.tree.traverse():
        old_file_path = os.path.join(old_dir, item.path)
        if item.type == "blob":  # 如果是文件
            with open(old_file_path, "wb") as f:
                f.write(item.data_stream.read())
        else:  # 如果是目录
            os.makedirs(old_file_path, exist_ok=True)
    
    # 将当前版本的文件复制到 new 目录中
    new_dir = os.path.join(working_dir, "new")
    shutil.copytree(repo.working_dir, new_dir)


def split_csv(file_path, result_dir):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        lines = list(reader)

    split_index = [i for i, row in enumerate(lines) if row[0] == '--------'][0]

    with open(os.path.join(result_dir, 'CloneSet.csv'), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(lines[:split_index])

    with open(os.path.join(result_dir, 'Clone.csv'), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(lines[split_index+1:])

    

# repo_path = r"C:\Users\admin\Code\undergraduate-thesis\case\dbeaver"
# working_dir = r"C:\Users\admin\Code\undergraduate-thesis\case\application"
# extract_previous_version(repo_path, working_dir)
