import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.List;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;

public class VirtualFileSystem {
    private ZipFile zipFile;
    private String currentDir;

    public VirtualFileSystem(String vfsPath) {
        try {
            zipFile = new ZipFile(vfsPath);
            currentDir = "";
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public String ls() {
        List<String> files = new ArrayList<>();
        Enumeration<? extends ZipEntry> entries = zipFile.entries();
        while (entries.hasMoreElements()) {
            ZipEntry entry = entries.nextElement();
            if (entry.getName().startsWith(currentDir)) {
                files.add(entry.getName().replaceFirst(currentDir, ""));
            }
        }
        return String.join("\n", files);
    }

    public void cd(String path) {
        if (path.equals("..")) {
            currentDir = Paths.get(currentDir).getParent().toString();
        } else {
            String newDir = Paths.get(currentDir, path).toString();
            ZipEntry entry = zipFile.getEntry(newDir);
            if (entry != null && entry.isDirectory()) {
                currentDir = newDir;
            } else {
                System.out.println("Directory " + path + " not found");
            }
        }
    }

    public void exit() {
        try {
            zipFile.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public String uname() {
        return "VirtualOS";
    }

    public void tac(String filePath) {
        try {
            ZipEntry entry = zipFile.getEntry(filePath);
            if (entry != null) {
                List<String> lines = new ArrayList<>();
                try (BufferedReader reader = new BufferedReader(new InputStreamReader(zipFile.getInputStream(entry)))) {
                    String line;
                    while ((line = reader.readLine()) != null) {
                        lines.add(line);
                    }
                }
                for (int i = lines.size() - 1; i >= 0; i--) {
                    System.out.println(lines.get(i));
                }
            } else {
                System.out.println("File " + filePath + " not found");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public String getCurrentDir() {
        return currentDir;
    }
}
