# 9ding backend

## Deployment

- run `init.py`
- **replace `key`,`salt`,`fifofile` with your own.**
- add configs in uwsgi config:

```config
master-fifo=your/path/to/fifo/file
master = true
processes = 1  # 单worker确保只有一个更新线程
threads = 2
lazy-apps = true  # 确保每个worker独立初始化
```

- put your model file(.glb) into folder `models` before running app.
