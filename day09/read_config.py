def load_config(path="config.txt"):
    cfg = {}
    try:
        with open(path, "r",encoding="utf") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                key,value = line.split("=",1)
                cfg[key.strip()] = value.strip()
        return cfg
    except FileNotFoundError:
        print(f"配置文件没有找到：{path}")
        return {}
if __name__ == "__main__":
    config = load_config()
    print(config)