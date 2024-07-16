if __name__ == '__main__':
    from app_multi import app
    try:
        app.run()
    except KeyboardInterrupt:
        app.stop_threads()
        app.cleanup()
        print("Exiting")