import os
import json
import threading


class Config():
    def __init__(self, filepath, init={}):
        self.path = filepath
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                f.write(json.dumps(init))
        with open(self.path, "r") as f:
            self.data = json.loads(f.read())
        self.lock = threading.Lock()

    def __getitem__(self, index):
        return self.data[index]

    def set(self, newdata):
        self.lock.acquire()
        self.data = newdata
        with open(self.path, "w") as f:
            f.write(json.dumps(self.data))
        self.lock.release()


picconfig = Config("./configs/pic.json", {
    "escape": True,
    "screens": [
        [
            [
                1480,
                860
            ],
            [
                0.25,
                1.75,
                -1.23
            ],
            [
                0,
                90,
                0
            ]
        ],
        [
            [
                1480,
                860
            ],
            [
                0.25,
                1.75,
                -3.0
            ],
            [
                0,
                90,
                0
            ]
        ],
        [
            [
                1480,
                860
            ],
            [
                0.25,
                1.75,
                -4.77
            ],
            [
                0,
                90,
                0
            ]
        ],
        [
            [
                2280,
                1260
            ],
            [
                3.65,
                1.75,
                -6.85
            ],
            [
                0,
                0,
                0
            ]
        ],
        [
            [
                1620,
                1000
            ],
            [
                6.73,
                1.5,
                -6.89
            ],
            [
                0,
                0,
                0
            ]
        ],
        [
            [
                3801,
                1620
            ],
            [
                9.5234,
                1.5,
                -6.846
            ],
            [
                0,
                0,
                0
            ]
        ],
        [
            [
                1620,
                1000
            ],
            [
                12.35,
                1.5,
                -6.85
            ],
            [
                0,
                0,
                0
            ]
        ]
    ],
    "info": [
        {
            "key": "stu_name",
            "display": "学生姓名",
            "default": "佚名"
        },
        {
            "key": "category",
            "display": "类别",
            "default": "未知"
        },
        {
            "key": "work_name",
            "display": "作品名称",
            "default": "无名"
        },
        {
            "key": "teacher",
            "display": "指导老师",
            "default": "佚名"
        }
    ],
    "delay": {
        "update": 500,
        "change": 5000
    },
    "loadTimeout": 100000,
    "text": {
        "font": {
            "color": "black",
            "size": "30px",
                    "famliy": "Simihei"
        },
        "position": {
            "x": 50,
            "down-padding": 20
        }
    },
    "backgroundColor": "#c7e8ff"
})
