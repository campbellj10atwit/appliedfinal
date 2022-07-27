from unittest import mock
from unittest import TestCase
import a5
import sqlite3
con = sqlite3.connect("assignment3.db")
cur = con.cursor()


class Tests(TestCase):

    @mock.patch('a5.input', create=True)
    def test_check_valid(self, mocked_input):
        
        mocked_input.side_effect = ['admin rubinv 1234']
        result = a5.req_login()
        self.assertEqual(result, ('admin', 'rubinv', True))
    
    
    @mock.patch('a5.input', create=True)
    def test_check_invalid(self, mocked_input):
        
        mocked_input.side_effect = ['admin rubinv abc']
        result = a5.req_login()
        self.assertFalse(result)
    
    @mock.patch('a5.input', create=True)
    def test_course_search(self,mocked_input):
        mocked_input.side_effect = ['bsco']
        result = a5.search_course()
        self.assertEqual(result,[(12345, 'Applied Programming Concepts', 'BSCO', '1:00-3:00', 'T, R', 'Summer', 2022, 3, 'Nelson Patrick', 2, '10001, 10002, ', 2)])

    def test_course_list(self):

        result = a5.course_list()
        self.assertEqual(result, [(12345, 'Applied Programming Concepts', 'BSCO', '1:00-3:00', 'T, R', 'Summer', 2022, 3, 'Nelson Patrick', 2, '10001, 10002, ', 2), (12347, 'test case', 'ELEC', '8:00-9:00', 'W', 'summer', 2022, 4, 'null', 10, '10001, 10002, ', 2)])

    @mock.patch('a5.input', create=True)
    def test_create_admin(self, mocked_input):

        mocked_input.side_effect = ['admin', '30003 test case', 'test role', 'test office',]
        result = a5.create_user()
        self.assertTrue(result)

    @mock.patch('a5.input', create=True)
    def test_create_student(self, mocked_input):

        mocked_input.side_effect = ['student', '10011 test case', '2023', 'bsco',]
        result = a5.create_user()
        self.assertTrue(result)

    @mock.patch('a5.input', create=True)
    def test_create_instructor(self, mocked_input):

        mocked_input.side_effect = ['instructor', '20007 test case', 'test professor', '1990', 'bsco']
        result = a5.create_user()
        self.assertTrue(result)
        
    @mock.patch('a5.input', create=True)
    def test_remove_admin(self, mocked_input):

        mocked_input.side_effect = ['admin', '30003']
        result = a5.remove_user()
        self.assertTrue(result)

    @mock.patch('a5.input', create=True)
    def test_remove_student(self, mocked_input):

        mocked_input.side_effect = ['student', '10011']
        result = a5.remove_user()
        self.assertTrue(result)

    @mock.patch('a5.input', create=True)
    def test_remove_instructor(self, mocked_input):

        mocked_input.side_effect = ['instructor', '20007']
        result = a5.remove_user()
        self.assertTrue(result)

    @mock.patch('a5.input', create=True)
    def test_add_course(self, mocked_input):

        mocked_input.side_effect = ['12346', 'test class', 'elec', '8:00-9:00', 'm, w', 'Summer 2022', '4', '10']
        result = a5.add_course()
        self.assertTrue(result)

    @mock.patch('a5.input', create=True)
    def test_remove_course(self, mocked_input):

        mocked_input.side_effect = ['12346']
        result = a5.remove_course()
        self.assertTrue(result)

    @mock.patch('a5.input', create=True)
    def test_croster(self, mocked_input):

        mocked_input.side_effect = ['12345']
        result = a5.croster()
        self.assertEqual(result, [('10001, 10002, ',)])
    
    @mock.patch('a5.input', create=True)
    def test_add_student(self, mocked_input):

        mocked_input.side_effect = ['12347', '10003']
        result = a5.add_student()
        self.assertEqual(result, '12347, ',)

    @mock.patch('a5.input', create=True)
    def test_add_student_already_in(self, mocked_input):

        mocked_input.side_effect = ['12347', '10002']
        result = a5.add_student()
        self.assertEqual(result, False)
    
    @mock.patch('a5.input', create=True)
    def test_add_student_class_full(self, mocked_input):

        mocked_input.side_effect = ['12345', '10002']
        result = a5.add_student()
        self.assertEqual(result, False)

    @mock.patch('a5.input', create=True)
    def test_remove_student(self, mocked_input):

        mocked_input.side_effect = ['12347', '10002']
        result = a5.remove_student()
        self.assertEqual(result, True)
    
    @mock.patch('a5.input', create=True)
    def test_remove_student_not_in(self, mocked_input):

        mocked_input.side_effect = ['12347', '10003']
        result = a5.remove_student()
        self.assertEqual(result, False)
    
    @mock.patch('a5.input', create=True)
    def test_find_prof(self, mocked_input):
        mocked_input.side_effect = ['bsco']
        result = a5.find_prof()
        self.assertEqual(result, [('Nelson', 'Patrick', 20002), ('Alan', 'Turing', 20004)])
    
    @mock.patch('a5.input', create=True)
    def test_find_prof_non(self, mocked_input):
        mocked_input.side_effect = ['elec']
        result = a5.find_prof()
        self.assertEqual(result, False) 
    
    @mock.patch('a5.input', create=True)
    def test_add_prof(self, mocked_input):
        mocked_input.side_effect = ['12345', '20004']
        result = a5.add_prof()
        self.assertEqual(result, True)



con.commit()
con.close()
