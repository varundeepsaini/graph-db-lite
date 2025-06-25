#!/usr/bin/env python3
"""
Test script for GraphDBLite CLI
This script tests the CLI functionality by simulating user commands
"""

import os
import sys
import tempfile
import shutil
from io import StringIO
from typing import Optional
from unittest.mock import patch
from cli.cli import GraphDBLiteCLI
from main import process_command
from utils.constants import save_file_path

class CLITester:
    def __init__(self):
        self.test_results = []
        self.temp_dir = tempfile.mkdtemp()
        self.backup_file = None
        
    def setup(self):
        """Setup test environment"""
        print("Setting up test environment...")
        
        # Backup existing data file if it exists
        if os.path.exists(save_file_path):
            self.backup_file = f"{save_file_path}.backup"
            shutil.copy2(save_file_path, self.backup_file)
            print(f"Backed up existing data to {self.backup_file}")
        
        # Create a fresh CLI instance
        self.cli = GraphDBLiteCLI()
        print("Test environment ready.")
        
    def teardown(self):
        """Cleanup test environment"""
        print("Cleaning up test environment...")
        
        # Restore original data file
        if self.backup_file and os.path.exists(self.backup_file):
            shutil.move(self.backup_file, save_file_path)
            print("Restored original data file")
        
        # Clean up temp directory
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        print("Test environment cleaned up.")
        
    def test_command(self, command: str, expected_success: bool = True, expected_output_contains: Optional[str] = None):
        """Test a single command"""
        print(f"\nTesting command: {command}")
        
        # Capture output
        with patch('sys.stdout', new=StringIO()) as fake_out:
            success = process_command(self.cli, command)
            output = fake_out.getvalue()
        
        # Check success/failure
        if success == expected_success:
            print(f"✓ Success/failure check passed")
        else:
            print(f"✗ Success/failure check failed. Expected: {expected_success}, Got: {success}")
            self.test_results.append(False)
            return False
        
        # Check output content if specified
        if expected_output_contains is not None:
            if expected_output_contains in output:
                print(f"✓ Output contains expected text: '{expected_output_contains}'")
            else:
                print(f"✗ Output does not contain expected text: '{expected_output_contains}'")
                print(f"  Actual output: {output.strip()}")
                self.test_results.append(False)
                return False
        
        print(f"✓ Command test passed")
        self.test_results.append(True)
        return True
    
    def run_tests(self):
        """Run all tests"""
        print("=" * 60)
        print("GraphDBLite CLI Test Suite")
        print("=" * 60)
        
        try:
            self.setup()
            
            # Test 1: Create a graph
            print("\n" + "="*40)
            print("Test 1: Graph Creation")
            print("="*40)
            self.test_command("CREATE GRAPH g1 DIRECTED WEIGHTED", True, "Created graph 'g1'")
            
            # Test 2: Create another graph
            self.test_command("CREATE GRAPH g2", True, "Created graph 'g2'")
            
            # Test 3: Try to create duplicate graph (should fail)
            self.test_command("CREATE GRAPH g1", False, "already exists")
            
            # Test 4: Add nodes
            print("\n" + "="*40)
            print("Test 2: Node Operations")
            print("="*40)
            self.test_command("ADD NODE g1 alice", True, "Added node 'alice'")
            self.test_command("ADD NODE g1 bob", True, "Added node 'bob'")
            self.test_command("ADD NODE g1 charlie", True, "Added node 'charlie'")
            self.test_command("ADD NODE g2 dave", True, "Added node 'dave'")
            
            # Test 5: Add edges
            print("\n" + "="*40)
            print("Test 3: Edge Operations")
            print("="*40)
            self.test_command("ADD EDGE g1 alice bob 5", True, "Added edge from 'alice' to 'bob'")
            self.test_command("ADD EDGE g1 bob charlie 3", True, "Added edge from 'bob' to 'charlie'")
            self.test_command("ADD EDGE g2 dave dave 1", True, "Added edge from 'dave' to 'dave'")
            
            # Test 6: List operations
            print("\n" + "="*40)
            print("Test 4: List Operations")
            print("="*40)
            self.test_command("LIST GRAPHS", True, "g1")
            self.test_command("LIST GRAPHS", True, "g2")
            self.test_command("LIST NODES g1", True, "alice")
            self.test_command("LIST NODES g1", True, "bob")
            self.test_command("LIST NODES g1", True, "charlie")
            self.test_command("LIST EDGES g1", True, "alice")
            self.test_command("LIST EDGES g1", True, "bob")
            
            # Test 7: Describe graph
            print("\n" + "="*40)
            print("Test 5: Graph Description")
            print("="*40)
            self.test_command("DESCRIBE GRAPH g1", True, "Graph: g1")
            self.test_command("DESCRIBE GRAPH g1", True, "Directed: True")
            self.test_command("DESCRIBE GRAPH g1", True, "Weighted: True")
            
            # Test 8: Delete edge
            print("\n" + "="*40)
            print("Test 6: Edge Deletion")
            print("="*40)
            self.test_command("DEL EDGE g1 bob charlie 3", True, "Removed edge from 'bob' to 'charlie'")
            
            # Test 9: Delete node (newly implemented)
            print("\n" + "="*40)
            print("Test 7: Node Deletion (New Feature)")
            print("="*40)
            self.test_command("DEL NODE g1 charlie", True, "Removed node 'charlie'")
            
            # Verify node was removed
            self.test_command("LIST NODES g1", True, "alice")
            self.test_command("LIST NODES g1", True, "bob")
            # Should not contain charlie anymore
            with patch('sys.stdout', new=StringIO()) as fake_out:
                process_command(self.cli, "LIST NODES g1")
                output = fake_out.getvalue()
                if "charlie" not in output:
                    print("✓ Node deletion verified - charlie not in node list")
                    self.test_results.append(True)
                else:
                    print("✗ Node deletion failed - charlie still in node list")
                    self.test_results.append(False)
            
            # Test 10: Save graph (newly implemented)
            print("\n" + "="*40)
            print("Test 8: Graph Saving (New Feature)")
            print("="*40)
            test_file = os.path.join(self.temp_dir, "g1.json")
            self.test_command(f"SAVE GRAPH g1 {test_file}", True, "Saved graph 'g1'")
            
            # Verify file was created
            if os.path.exists(test_file):
                print("✓ Graph save verified - file created")
                self.test_results.append(True)
            else:
                print("✗ Graph save failed - file not created")
                self.test_results.append(False)
            
            # Test 11: Load graph
            print("\n" + "="*40)
            print("Test 9: Graph Loading")
            print("="*40)
            self.test_command(f"LOAD GRAPH {test_file}", True, "Loaded graph from")
            
            # Test 12: Error handling
            print("\n" + "="*40)
            print("Test 10: Error Handling")
            print("="*40)
            self.test_command("CREATE GRAPH", False, "Usage:") 
            self.test_command("ADD NODE nonexistent alice", False, "does not exist")  # Non-existent graph
            self.test_command("ADD NODE g1", False, "ERROR: Correct usage:")
            self.test_command("DEL NODE g1 nonexistent", False, "does not exist")  # Non-existent node
            
            # Test 13: Help command
            print("\n" + "="*40)
            print("Test 11: Help Command")
            print("="*40)
            self.test_command("HELP", True, "GraphDBLite - Lightweight Graph Database")
            
            # Test 14: Clear command
            print("\n" + "="*40)
            print("Test 12: Clear Command")
            print("="*40)
            self.test_command("CLEAR", True)
            
            # Test 15: Exit command
            print("\n" + "="*40)
            print("Test 13: Exit Command")
            print("="*40)
            self.test_command("EXIT", False)

            # Test 14: Edge Cases and Robustness
            print("\n" + "="*40)
            print("Test 14: Edge Cases and Robustness")
            print("="*40)
            # Add edge between non-existent nodes (should auto-create nodes)
            self.test_command("ADD EDGE g1 nonexist1 nonexist2 2", True, "Added edge from 'nonexist1' to 'nonexist2'")
            # Add node with invalid characters
            self.test_command("ADD NODE g1 alice!", False, "ERROR: Correct usage:")
            # Add edge with non-numeric weight in weighted graph
            self.test_command("ADD EDGE g1 alice bob notanumber", False, "ERROR: Correct usage:")
            # Add duplicate edge
            self.test_command("ADD EDGE g1 alice bob 5", False, "already exists")
            # Add duplicate node
            self.test_command("ADD NODE g1 alice", False, "already exists")
            # Add self-loop in undirected graph
            self.test_command("CREATE GRAPH g3", True, "Created graph 'g3'")
            self.test_command("ADD NODE g3 zed", True, "Added node 'zed'")
            self.test_command("ADD EDGE g3 zed zed", True, "Added edge from 'zed' to 'zed'")
            # Create graph with only DIRECTED
            self.test_command("CREATE GRAPH g4 DIRECTED", True, "Created graph 'g4'")
            # Create graph with only WEIGHTED
            self.test_command("CREATE GRAPH g5 WEIGHTED", True, "Created graph 'g5'")
            # Describe a graph with no nodes/edges
            self.test_command("DESCRIBE GRAPH g4", True, "Graph: g4")
            # Save, clear, and load a graph
            test_file2 = os.path.join(self.temp_dir, "g3.json")
            self.test_command(f"SAVE GRAPH g3 {test_file2}", True, "Saved graph 'g3'")
            self.test_command("CLEAR", True)
            self.test_command(f"LOAD GRAPH {test_file2}", True, "Loaded graph from")
            self.test_command("LIST NODES g3", True, "zed")
            # Load a non-existent file
            self.test_command("LOAD GRAPH /tmp/nonexistentfile.json", False, "Failed to load graph")
            # Delete a node with multiple edges
            self.test_command("CREATE GRAPH g6", True, "Created graph 'g6'")
            self.test_command("ADD NODE g6 a", True, "Added node 'a'")
            self.test_command("ADD NODE g6 b", True, "Added node 'b'")
            self.test_command("ADD NODE g6 c", True, "Added node 'c'")
            self.test_command("ADD EDGE g6 a b", True, "Added edge from 'a' to 'b'")
            self.test_command("ADD EDGE g6 a c", True, "Added edge from 'a' to 'c'")
            self.test_command("DEL NODE g6 a", True, "Removed node 'a'")
            self.test_command("LIST NODES g6", True, "b")
            self.test_command("LIST NODES g6", True, "c")
            # Delete a non-existent edge
            self.test_command("DEL EDGE g6 b c", False, "does not exist")
            # Delete a node from a graph with only one node
            self.test_command("CREATE GRAPH g7", True, "Created graph 'g7'")
            self.test_command("ADD NODE g7 solo", True, "Added node 'solo'")
            self.test_command("DEL NODE g7 solo", True, "Removed node 'solo'")
            # List nodes/edges in an empty graph
            self.test_command("LIST NODES g7", True)
            self.test_command("LIST EDGES g7", True)
            # List graphs when none exist (after clear)
            self.test_command("CLEAR", True)
            self.test_command("LIST GRAPHS", True)
            # Invalid command
            self.test_command("FOO BAR", False, "ERROR: Unknown command")
            # HELP, CLEAR, EXIT commands
            self.test_command("HELP", True, "GraphDBLite - Lightweight Graph Database")
            self.test_command("CLEAR", True)
            self.test_command("EXIT", False)

            print("\n" + "="*60)
            print("EDGE CASES & ROBUSTNESS TEST SUMMARY")
            print("="*60)
            total_tests = len(self.test_results)
            passed_tests = sum(self.test_results)
            failed_tests = total_tests - passed_tests
            print(f"Total tests: {total_tests}")
            print(f"Passed: {passed_tests}")
            print(f"Failed: {failed_tests}")
            print(f"Success rate: {(passed_tests/total_tests)*100:.1f}%")
            if failed_tests == 0:
                print("\n🎉 All edge case tests passed! GraphDBLite CLI is robust.")
            else:
                print(f"\n❌ {failed_tests} edge case test(s) failed. Please check the implementation.")
            
            # Print test summary
            print("\n" + "="*60)
            print("TEST SUMMARY")
            print("="*60)
            total_tests = len(self.test_results)
            passed_tests = sum(self.test_results)
            failed_tests = total_tests - passed_tests
            
            print(f"Total tests: {total_tests}")
            print(f"Passed: {passed_tests}")
            print(f"Failed: {failed_tests}")
            print(f"Success rate: {(passed_tests/total_tests)*100:.1f}%")
            
            if failed_tests == 0:
                print("\n🎉 All tests passed! GraphDBLite CLI is working correctly.")
                return True
            else:
                print(f"\n❌ {failed_tests} test(s) failed. Please check the implementation.")
                return False
                
        finally:
            self.teardown()

def main():
    """Main test runner"""
    tester = CLITester()
    success = tester.run_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 