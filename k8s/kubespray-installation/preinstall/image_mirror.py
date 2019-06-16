from jinja2 import Environment, FileSystemLoader
import yaml
import sys
import re

def replace(in_yml, repo_hub, out_yml):
    pattern = re.compile(r'\{\{ .*? \}\}')
    inp = open(in_yml)
    image_repo_tags = yaml.load(inp)
    inp.close()
    images = dict()
    for k in image_repo_tags:
        v = str(image_repo_tags[k])
        if "image_repo" in k:
            if "image_arch" in v:
                result = re.findall(pattern, v)
                if len(result) == 0:
                    images[k] = v[0:v.index("{")] + "-amd64"
                else:
                    for it in result:
                        key = it.strip("{}").strip()
                        val = image_repo_tags[key]
                        v = v.replace(it, val) 
                    
            else:
                images[k] = v
            image_repo_tags[k] = repo_hub + "/" + v.split("/")[-1]
        elif "image_tag" in k:
            if "image_arch" in v:
                version = v.split("}")[0].strip("{").strip() 
                images[k] = image_repo_tags[version] + "amd64"
            elif "{" in v:
                version = v.strip("{}").strip()
                images[k] = str(image_repo_tags[version])
            else:
                images[k] = str(image_repo_tags[k])
    out = open(out_yml, "w")
    yaml.dump(image_repo_tags, out)
    out.close()
    return images


def generate_mirror(old_imgs, repo_hub):
    pull = open("pull.sh", "w")
    push = open("push.sh", "w")
    for it in old_imgs:
        if "image_repo" in it:    
            image_tag = it.replace("image_repo", "image_tag")
            if image_tag in old_imgs:
                pull_str = old_imgs[it] + ":" + old_imgs[image_tag] 
                pull.write(pull_str + "\n")
                push_str = repo_hub + "/" + pull_str.split("/")[-1]
                push.write(push_str + "\n")
    pull.close()
    push.close()


if __name__ == '__main__':
    old_imgs = replace(sys.argv[1], "registry.cn-shenzhen.aliyuncs.com/zbpub", "out.yml") 
    generate_mirror(old_imgs, "registry.cn-shenzhen.aliyuncs.com/zbpub")
