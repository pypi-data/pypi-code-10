from boto.s3.connection import S3Connection

def main():
    conn = S3Connection()

    buckets = conn.get_all_buckets()

    for b in buckets:
        print b.name

if __name__ == "__main__":
    main()
