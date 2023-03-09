# pipelines.py
import os
import psycopg2


class NewsSpiderPipeline:

    def __init__(self):
        ## Connection Details
        hostname = os.environ.get('POSTGRES_HOST')
        username = os.environ.get('POSTGRES_USER')
        password = os.environ.get('POSTGRES_PASSWORD')
        database = os.environ.get('POSTGRES_DB')

        ## Create/Connect to database
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        
        ## Create cursor, used to execute commands
        self.cur = self.connection.cursor()
        
        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS news_articles(
            id serial PRIMARY KEY, 
            category text,
            title text,
            body text,
            image text,
            published_date DATE NOT NULL DEFAULT CURRENT_DATE,
            scraped_date DATE NOT NULL DEFAULT CURRENT_DATE
        )
        """)

    def process_item(self, item, spider):

        ## Check to see if text is already in database 
        self.cur.execute("select * from news_articles where title = %s", (item['articleTitle'],))
        result = self.cur.fetchone()

        ## If it is in DB, create log message
        if result:
            spider.logger.warn("Item already in database: %s" % item['articleTitle'])


        ## If text isn't in the DB, insert data
        else:

            ## Define insert statement
            self.cur.execute(""" insert into news_articles (category, title, body, image, published_date) values (%s,%s,%s,%s,%s)""", (
                item["articleCategory"],
                item["articleTitle"],
                item["articleBody"],
                item['imageLink'],
                item['published_date']


            ))

            ## Execute insert of data into database
            self.connection.commit()
        return item

    
    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.connection.close()



