import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

public class Config {
    private Properties properties;

    public Config(String configPath) {
        properties = new Properties();
        try (InputStream input = getClass().getClassLoader().getResourceAsStream(configPath)) {
            if (input == null) {
                System.out.println("Unable to find " + configPath);
                return;
            }
            properties.load(input);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public String getHostname() {
        return properties.getProperty("hostname");
    }

    public String getVfsPath() {
        return properties.getProperty("vfs_path");
    }

    public String getLogPath() {
        return properties.getProperty("log_path");
    }
}
