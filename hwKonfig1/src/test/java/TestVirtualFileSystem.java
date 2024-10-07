import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import static org.junit.jupiter.api.Assertions.*;

public class TestVirtualFileSystem {
    private VirtualFileSystem vfs;
    private final ByteArrayOutputStream outContent = new ByteArrayOutputStream();
    private final PrintStream originalOut = System.out;

    @BeforeEach
    public void setUp() {
        vfs = new VirtualFileSystem("vfs.zip");
        System.setOut(new PrintStream(outContent));
    }

    @AfterEach
    public void tearDown() {
        System.setOut(originalOut);
    }

    @Test
    public void testLs() {
        String files = vfs.ls();
        assertTrue(files.contains("file1.txt"));
        assertTrue(files.contains("dir1/file3.txt"));
    }

    @Test
    public void testCd() {
        vfs.cd("dir1");
        assertEquals("/dir1/", vfs.getCurrentDir());

        vfs.cd("..");
        assertEquals("/", vfs.getCurrentDir());
    }

    @Test
    public void testCdNonExistentDirectory() {
        vfs.cd("nonexistent");
        assertEquals("", vfs.getCurrentDir());
    }

    @Test
    public void testTac() {
        // Assuming 'file1.txt' contains "line1\nline2\nline3"
        vfs.tac("file1.txt");
        String output = outContent.toString().trim();
        assertEquals("line3\nline2\nline1", output);
    }

    @Test
    public void testTacNonExistentFile() {
        vfs.tac("nonexistent.txt");
        String output = outContent.toString().trim();
        assertEquals("File nonexistent.txt not found", output);
    }

    @Test
    public void testUname() {
        assertEquals("VirtualOS", vfs.uname());
    }
}
