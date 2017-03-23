#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import os.path
import random
import fileinput

def create_db():
	db = sqlite3.connect("database.db")
	cur = db.cursor()

	fd = open('database_scheme_and_data_12.sql', 'r')
	
	for line in fd.read().split(';\n'):
		cur.execute(line)
	db.commit()
	fd.close()
	db.close()

	# cur.execute("SELECT column_name from table_name LIMIT 11")
	# test = cur.fetchall()

	print "Database created!"


def main():
    if os.path.isfile("database.db"):
        print 'DB exists'
    else:
        create_db()

    if os.path.isfile("output.html"):
        os.remove("output.html")

    outfile = open("output.html", "a")

    test1 = "<!DOCTYPE html>\n<html>\n<head>\n<meta charset=\"utf-8\" />\n</head>\n<body>\n<h1>Amateurfunkprüfung</h1>\n<font face=\"verdana\">\n"

    outfile.write(test1)

    db = sqlite3.connect("database.db")
    cur = db.cursor()

    # cur.execute('SELECT _id FROM question_to_topic WHERE topic_id = 1')
    # cur.execute('SELECT question FROM question WHERE reference=?', t)

    ## Hier die Fragen eintragen aus denen das Arbeitsblatt bestehen soll ##
    fragen_liste = ['TD420', 'TB201', 'TD603', 'TD702', 'TE102']




    for frage in fragen_liste:
        t = (frage,)

        cur.execute("SELECT question,_id FROM question where reference=? AND _id IN (SELECT question_id FROM question_to_topic WHERE topic_id=2)",t)
        fragen_text = cur.fetchone()
        # print fragen_text[0]
        # print fragen_text[1]

        # print fragen_text[0].replace("img src='", "img src='drawable/")

        outfile.write("<p>" + "<b>" + frage + " </b>" + fragen_text[0].replace("img src='", "img src='drawable/").encode("utf-8") + "</p>")

        cur.execute("SELECT answer FROM answer WHERE question_id=? ORDER BY order_index",(fragen_text[1],))
        antworten_text = cur.fetchall()

        rnd_antworten = range(4)
        random.shuffle(rnd_antworten)
        # print rnd_antworten

        outfile.write("<p>\n")
        for nb in rnd_antworten:
            # print nb

            outfile.write("&#9744;" + "<FONT SIZE=\"-1\">" + antworten_text[nb][0].replace("img src='", "img src='drawable/").encode("utf-8") + "</font><br>")
            # print antworten_text[nb]
        outfile.write("</p>")

    outfile.write("</font>\n</body>\n</html>")
    db.close()
    outfile.close()

    print "Ende!"

if __name__ == "__main__":
    main()