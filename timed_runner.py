import time

INTERVAL = 300  # 5分钟

def run_local():
    import localrun
    localrun.main()

if __name__ == "__main__":
    while True:
        now = time.time()
        # 计算下一个5分钟整点
        next_run = ((now // INTERVAL) + 1) * INTERVAL
        run_local()
        # 运行结束后sleep到下一个5分钟点
        sleep_time = max(0, next_run - time.time())
        if sleep_time > 0:
            time.sleep(sleep_time)
