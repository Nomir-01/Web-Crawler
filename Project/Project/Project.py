from urllib.request import Request, urlopen, URLError, urljoin
import time
import threading
import queue
from bs4 import BeautifulSoup
import ssl

class Crawler(threading.Thread):
    def __init__(self,url,css_tag,tag_info,css_selector,crawling_links,visited_links,error_links,url_lock):
        threading.Thread.__init__(self)
        self.url=url
        self.css_tag=css_tag
        self.tag_info=tag_info
        self.css_selector=css_selector
        self.crawling_links=crawling_links
        self.visited_links=visited_links
        self.error_links=error_links
        self.url_lock=url_lock
        
    def run(self):
        my_ssl=ssl.create_default_context()
        my_ssl.check_hostname=False
        my_ssl.verify_mode=ssl.CERT_NONE
        while True:
            self.url_lock.acquire()
            link=self.crawling_links.get()
            self.url_lock.release()
            if link is None:
                break
            if link in self.visited_links:
                print(f"The URL {link} Is Visited")
                break
            try:
                link=urljoin(self.url,link)
                req=Request(link, headers={'User-Agent':'Mozilla/5.0'})
                response=urlopen(req,context=my_ssl)
                print(f"The URL {response.geturl()} Crawled With Status {response.getcode()}")
                soup=BeautifulSoup(response.read(),"html.parser")
                if self.css_selector is None:
                    for tag in soup.find_all(self.css_tag):
                        if (tag.get("href") not in self.visited_links):
                            self.crawling_links.put(tag.get("href"))
                        else:
                            href=urljoin(self.url,tag.get("href"))
                            title=tag.string
                            if(self.tag_info=='href'):
                                print(f"\nThe URL {href} Is Visited")
                            elif(self.tag_info=='title'):
                                print(f"\nThe URL {title} Is Visited")
                else:
                    all_links=soup.select(self.css_selector)
                    for tag in all_links:
                        if (tag.get("href") not in self.visited_links):
                            self.crawling_links.put(tag.get("href"))
                        else:
                            href=urljoin(self.url,tag.get("href"))
                            print(f"\nThe URL {href} Is Visited")
                print(f"\n{link} Is Added To The Crawled List")
                self.visited_links.add(link)
            except URLError as e:
                print(f"\nThe Given URL Threw Error : {e.reason} ")
                self.error_links.append(link)
            finally:
                self.crawling_links.task_done()

def Base_1():
    f=open("Base1_Links.txt","r")
    print(f.read())
    f=open("Base1_Links.txt","a")
    url=input("Please Enter URL To Crawl : ")
    f.write("\n"+url+"\n")
    f.close
    threads=input("\nPlease Enter The Number Of Threads : ")
    print("\nPlease Select A Css Tag : \n\n1.'a'\t\t2.'div'\n\n3.'p'\t\t4.'h'\n\nYou Can Also Enter Your Own Css Tag")
    choice=input("\nPlease Enter Your Choice : ")
    if(choice=='1'):
        css_tag='a'
    elif(choice=='2'):
        css_tag='div'
    elif(choice=='3'):
        css_tag='p'
    elif(choice=='4'):
        css_tag='h'
    else:
        css_tag=choice
    print("\nPlease Select If You Want Links Inside The Selected Tag OR The Text Between The Selected Tags : \n\n1.Links Inside The Selected Tag(href)\n2.The Text Between The Selected Tags(Title)")
    choice=input("\nPlease Enter Your Choice : ")
    if(choice=='1'):
        tag_info='href'
    elif(choice=='2'):
        tag_info='title'
    print("")
    css_selector=None
    crawling_links=queue.Queue()
    url_lock=threading.Lock()
    crawling_links.put(url)
    visited_links=set()
    crawling_threads=[]
    error_links=[]
    start_time=time.time()
    for i in range(int(threads)):
        crawler=Crawler(url=url,css_tag=css_tag,tag_info=tag_info,css_selector=css_selector,crawling_links=crawling_links,visited_links=visited_links,error_links=error_links,url_lock=url_lock)
        crawler.start()
        crawling_threads.append(crawler)
    for crawler in crawling_threads:
        crawler.join()
    end_time=time.time()-start_time
    visited=len(visited_links)
    errors=len(error_links)
    print("\n=======================================================================================================================\n")
    print(f"URL : {url}")
    print(f"Total Threads : {threads}")
    print(f"Total Time Taken : {end_time}")
    print(f"Total Number Of Visited Pages : {visited}")
    print(f"Total Number Of Links With Errors : {errors}\n")
    print("=======================================================================================================================\n")
    f=open("Base1_Links_With_Info.txt","r")
    print(f.read())
    f=open("Base1_Links_With_Info.txt","a")
    f.write("\nURL : "+url+"\nThreads : "+threads+"\nTime : "+str(end_time)+"\nVisited Pages : "+str(visited)+"\nLinks With Errors : "+str(errors)+"\n")
    f.close
    print("=======================================================================================================================\n")
    print("Do You Want To Crawl Another Webpage(Y/N) : ")
    choice=input("\nPlease Enter Your Choice : ")
    print("")
    if(choice=='Y' or choice=='y'):
        Home()
    elif(choice=='N' or choice=='n'):
        exit

def Base_2():
    f=open("Base2_Links.txt","r")
    print(f.read())
    f=open("Base2_Links.txt","a")
    url=input("\nPlease Enter URL To Crawl : ")
    f.write("\n"+url+"\n")
    f.close
    threads=input("\nPlease Enter The Number Of Threads : ")
    css_selector=input("\nPlease Enter Your Css Selector : ")
    print("")
    css_tag=None
    tag_info=None
    crawling_links=queue.Queue()
    url_lock=threading.Lock()
    crawling_links.put(url)
    visited_links=set()
    crawling_threads=[]
    error_links=[]
    start_time=time.time()
    for i in range(int(threads)):
        crawler=Crawler(url=url,css_tag=css_tag,tag_info=tag_info,css_selector=css_selector,crawling_links=crawling_links,visited_links=visited_links,error_links=error_links,url_lock=url_lock)
        crawler.start()
        crawling_threads.append(crawler)
    for crawler in crawling_threads:
        crawler.join()
    end_time=time.time()-start_time
    visited=len(visited_links)
    errors=len(error_links)
    print("\n========================================================================================================================\n")
    print(f"URL : {url}")
    print(f"Total Threads : {threads}")
    print(f"Total Time Taken : {end_time}")
    print(f"Total Number Of Visited Pages : {visited}")
    print(f"Total Number Of Links With Errors : {errors}\n")
    print("========================================================================================================================\n")
    f=open("Base2_Links_With_Info.txt","r")
    print(f.read())
    f=open("Base2_Links_With_Info.txt","a")
    f.write("\nURL : "+url+"\nThreads : "+threads+"\nTime : "+str(end_time)+"\nVisited Pages : "+str(visited)+"\nLinks With Errors : "+str(errors)+"\n")
    f.close
    print("========================================================================================================================\n")
    print("Do You Want To Crawl Another Webpage(Y/N) : ")
    choice=input("\nPlease Enter Your Choice : ")
    print("")
    if(choice=='Y' or choice=='y'):
        Home()
    elif(choice=='N' or choice=='n'):
        exit

def Home():
    print("\t\t\t\t\t\t==========================")
    print("\t\t\t\t\t\tMulti Threaded Web Crawler")
    print("\t\t\t\t\t\t==========================")
    print("Do You Want To Use Your Own Css Selector(Y/N) : ")
    choice=input("\nPlease Enter Your Choice : ")
    print("")
    if(choice=='Y' or choice=='y'):
        Base_2()
    elif(choice=='N' or choice=='n'):
        Base_1()

Home()