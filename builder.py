import os
from zipfile import ZipFile
import configparser
import json

config_file = 'build_config.ini'


def start_config_worker():
    global config_file
    config = configparser.ConfigParser()
    config.read(config_file)
    if not config.has_section("BuildSettings"):
        config.add_section("BuildSettings")
    if not config.has_option("BuildSettings", "assets_dir"):
        config.set("BuildSettings", "assets_dir", "src/assets")
    if not config.has_option("BuildSettings", "build_dir"):
        config.set("BuildSettings", "build_dir", "build")
    if not config.has_section("PackSettings"):
        config.add_section("PackSettings")
    if not config.has_option("PackSettings", "pack_name"):
        config.set("PackSettings", "pack_name", "LogicResources")
    if not config.has_option("PackSettings", "pack_version"):
        config.set("PackSettings", "pack_version", "1.0")
    if not config.has_option("PackSettings", "pack_format"):
        config.set("PackSettings", "pack_format", "3")
    if not config.has_option("PackSettings", "description"):
        config.set("PackSettings", "description",
                   "§fLogicResources32§r for §fJava Edition§r.\n§6Authors:§r §cxLogicWorlds")

    with open(config_file, "w") as config_f:
        config.write(config_f)


def start_pre_build_phase():
    global config_file
    config = configparser.ConfigParser()
    if not os.path.exists(config_file):
        print("Error open file!")

    config.read(config_file)

    assets_dir = config.get("BuildSettings", "assets_dir")
    if not os.path.exists(assets_dir):
        print("assets_dir: '{a1}' not found!".format(a1=assets_dir))
        exit()
    b_dir = config.get("BuildSettings", "build_dir")
    if not os.path.exists(str(b_dir)):
        os.mkdir(b_dir)
    if not os.path.exists(str(b_dir + "/temp")):
        os.mkdir(b_dir + "/temp")
    if not os.path.exists(str(b_dir + "/result")):
        os.mkdir(b_dir + "/result")


def get_config_param(section, param):
    global config_file
    config = configparser.ConfigParser()
    config.read(config_file)
    if config.has_option(section, param):
        return config.get(section, param)
    else:
        return None


def convert_all_xcf():
    print('WIP')

def create_pack_meta():
    pre_json = {
        'pack':{
           'pack_format': int(get_config_param("PackSettings", "pack_format")),
            'description': get_config_param("PackSettings", "description")
        }
    }
    json_meta = json.dumps(pre_json, sort_keys=True, indent=4)

    meta_file_path = get_config_param("BuildSettings", "build_dir")+'/temp/pack.mcmeta'
    with open(meta_file_path, "w") as config_f:
        config_f.write(json_meta)

def append_files():
    build_dir = get_config_param("BuildSettings", "build_dir")
    assets_dir = get_config_param("BuildSettings", "assets_dir")
    tmp_dir = build_dir + "/temp"
    pack_name = get_config_param("PackSettings", "pack_name")
    pack_version = get_config_param("PackSettings", "pack_version")
    result_filename = build_dir + "/result/{name}-{version}.zip".format(name=pack_name, version=pack_version)
    if os.path.exists(result_filename):
        os.remove(result_filename)
    result_zip = ZipFile(result_filename, 'w')
    for root, dirs, files in os.walk('src'):
        for file in files:
            if (root + file).endswith('.png'):
                # print('Append file: ', root + file)
                path = os.path.join(root + "/" + file)
                result_path = path[len(assets_dir) - 6:]
                print('Append file:', result_path)
                result_zip.write(path, result_path)
    # Add mcmeta
    print('Generate pack.mcmeta')
    create_pack_meta()
    print('Append pack.mcmeta')
    result_zip.write(build_dir+'/temp/pack.mcmeta', 'pack.mcmeta')


def end_compile():
    b_dir = get_config_param("BuildSettings", "build_dir")
    print("Remove temp files...")
    if os.path.exists(str(b_dir + "/temp")):
        os.remove(b_dir + "/temp/pack.mcmeta")
        os.rmdir(b_dir + "/temp")


# Work with config_file
# Check configs and create build folders
start_config_worker()
start_pre_build_phase()
# Start compile
print("Starting build process...")
append_files()
end_compile()
print("COMPILATION COMPLETE!")
