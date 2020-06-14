import unittest
from unittest import TestCase
import mysql.connector
from sshtunnel import SSHTunnelForwarder
import bcrypt
import smtplib, ssl


class Testdatabase(unittest.TestCase):

    def test_username(self):
        server = SSHTunnelForwarder(
            '146.141.21.92',
            ssh_username='s1533169',
            ssh_password='dingun123',
            remote_bind_address=('127.0.0.1', 3306)
        )
        server.start()

        mydb = mysql.connector.connect(host="localhost",user="s1533169",passwd="dingun123" ,port=server.local_bind_port)
        mycursor= mydb.cursor()

        mycursor.execute("USE d1533169")
        inUserName = 'nicci'
        inUserPassword = '$2b$12$Mq5OFNhPsxOYvB2zfWOgOedq40kAn/hCIn.9dS47jtXQnzOcq3V1q'
        mycursor.execute("SELECT * FROM ARIMA_USERS WHERE USERNAME=%s",(inUserName.strip(),))


        myresult=mycursor.fetchall()
        myresultusername = myresult[0][0]
        self.assertEqual(myresultusername, "nicci")

    def test_email(self):
        server = SSHTunnelForwarder(
            '146.141.21.92',
            ssh_username='s1533169',
            ssh_password='dingun123',
            remote_bind_address=('127.0.0.1', 3306)
        )
        server.start()

        mydb = mysql.connector.connect(host="localhost",user="s1533169",passwd="dingun123" ,port=server.local_bind_port)
        mycursor= mydb.cursor()

        mycursor.execute("USE d1533169")
        inUserName = 'nicci'
        inUserPassword = '$2b$12$Mq5OFNhPsxOYvB2zfWOgOedq40kAn/hCIn.9dS47jtXQnzOcq3V1q'
        mycursor.execute("SELECT * FROM ARIMA_USERS WHERE USERNAME=%s",(inUserName.strip(),))


        myresult=mycursor.fetchall()
        myresultemail = myresult[0][2]
        self.assertEqual(myresultemail, "nicholasbaard30@gmail.com")

    def test_password(self):
        server = SSHTunnelForwarder(
            '146.141.21.92',
            ssh_username='s1533169',
            ssh_password='dingun123',
            remote_bind_address=('127.0.0.1', 3306)
        )
        server.start()

        mydb = mysql.connector.connect(host="localhost",user="s1533169",passwd="dingun123" ,port=server.local_bind_port)
        mycursor= mydb.cursor()

        mycursor.execute("USE d1533169")
        inUserName = 'nicci'
        inUserPassword = '$2b$12$Mq5OFNhPsxOYvB2zfWOgOedq40kAn/hCIn.9dS47jtXQnzOcq3V1q'
        mycursor.execute("SELECT * FROM ARIMA_USERS WHERE USERNAME=%s",(inUserName.strip(),))


        myresult=mycursor.fetchall()
        myresultpassword = myresult[0][1]
        self.assertEqual(myresultpassword.encode('utf-8'), inUserPassword.encode('utf-8'))

    def test_connection(self):
        server = SSHTunnelForwarder(
            '146.141.21.92',
            ssh_username='s1533169',
            ssh_password='dingun123',
            remote_bind_address=('127.0.0.1', 3306)
        )
        server.start()

        mydb = mysql.connector.connect(host="localhost",user="s1533169",passwd="dingun123" ,port=server.local_bind_port)
        mycursor= mydb.cursor()

        mycursor.execute("USE d1533169")
        inUserName = 'nicci'
        inUserPassword = '$2b$12$Mq5OFNhPsxOYvB2zfWOgOedq40kAn/hCIn.9dS47jtXQnzOcq3V1q'
        mycursor.execute("SELECT * FROM ARIMA_USERS WHERE USERNAME=%s",(inUserName.strip(),))


        myresult=mycursor.fetchall()
        self.assertEqual(len(myresult[0]), 3)

if __name__ == '__main__':
    unittest.main()
