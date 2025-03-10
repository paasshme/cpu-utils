import unittest
from io import StringIO
import sys

# Assuming the assembler code is in a file named `assembler.py`
from assembler_16_ins_4_bit_pc import (
    handle_3_operands, handle_immediate, handle_jumps, handle_others,
    translate_labels, check_instruction_limit, preassemble, assemble,
    handle_memy
)

TEST_FOLDER="test_files"

class TestAssembler(unittest.TestCase):

    def setUp(self):
        # Redirect stdout to capture print statements
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        # Reset stdout
        sys.stdout = sys.__stdout__

    def test_handle_3_operands(self):
        self.assertEqual(handle_3_operands("ADD", ["r1", "r2", "r3"]), "0001000100100011")
        self.assertEqual(handle_3_operands("SUB", ["r4", "r5", "r6"]), "0010010001010110")
        self.assertEqual(handle_3_operands("AND", ["r4", "r3", "r2"]), "0110010000110010")

    def test_handle_immediate(self):
        self.assertEqual(handle_immediate("LDI", ["r1", "42"]), "1000000100101010")
        self.assertEqual(handle_immediate("LDI", ["r4", "10"]), "1000010000001010")
        self.assertEqual(handle_immediate("ADI", ["r2", "255"]), "1010001011111111")

    def test_handle_jumps(self):
        self.assertEqual(handle_jumps("JMP", 5), "1011000000000101")
        self.assertEqual(handle_jumps("BRZ", 1), "1100010000000001")
        self.assertEqual(handle_jumps("BRNZ", 2), "1100110000000010")
        self.assertEqual(handle_jumps("BRNC", 3), "1100000000000011")
        self.assertEqual(handle_jumps("BRC", 4), "1100100000000100")
        self.assertEqual(handle_jumps("CALL", 7), "1101000000000111")
        self.assertEqual(handle_jumps("RET", None), "1110000000000000")

    def test_handle_memy(self):
        self.assertEqual(handle_memy("ST", "r1","r2","3"), "1111000100100011")
        self.assertEqual(handle_memy("ST", "r4","r2","3"), "1111010000100011")
        self.assertEqual(handle_memy("LB", "r4","r2","3"), "0100010000100011")
        self.assertEqual(handle_memy("LB", "r1","r2","3"), "0100000100100011")

    def test_translate_labels(self):
        datas = [".label1:\n", "ADD r1 r2 r3\n", "JMP label1\n", "BRZ label1\n"]
        labels = translate_labels(datas)
        self.assertEqual(labels, {".label1": 0})

    def test_check_instruction_limit(self):
        datas = ["# Comment\n", "ADD r1 r2 r3\n"] * 10
        self.assertTrue(check_instruction_limit(datas))
        datas = ["ADD r1 r2 r3\n"] * 17
        self.assertFalse(check_instruction_limit(datas))

    def test_preassemble(self):
        with open(f"{TEST_FOLDER}/test_input.as", "w") as f:
            f.write(".label:\nADD r1 r2 r3\nJMP 0\n")
        preassemble(f"{TEST_FOLDER}/test_input.as", f"{TEST_FOLDER}/test_output.asx")
        with open(f"{TEST_FOLDER}/test_output.asx", "r") as f:
            output = f.read()
        self.assertIn("0 ADD r1 r2 r3", output)
        self.assertIn("1 JMP 0", output)

    def test_assemble(self):
        with open(f"{TEST_FOLDER}/test_input.as", "w") as f:
            f.write("ADD r1 r2 r3\nLDI r4 10\nHALT\n")
        assemble(f"{TEST_FOLDER}/test_input.as", f"{TEST_FOLDER}/test_output.bin")
        with open(f"{TEST_FOLDER}/test_output.bin", "r") as f:
            output = f.read()
        self.assertIn("0001000100100011", output)
        self.assertIn("1001000000000000", output)
        self.assertIn("1000010000001010", output)

if __name__ == '__main__':
    unittest.main()
