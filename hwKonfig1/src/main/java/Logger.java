import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.reflect.TypeToken;

import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.lang.reflect.Type;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Logger {
    private String logPath;
    private Gson gson;

    public Logger(String logPath) {
        this.logPath = logPath;
        this.gson = new GsonBuilder().setPrettyPrinting().create();
    }

    public void logAction(String command) {
        try (FileWriter writer = new FileWriter(logPath, true)) {
            Map<String, String> logEntry = new HashMap<>();
            logEntry.put("timestamp", LocalDateTime.now().toString());
            logEntry.put("command", command);
            writer.write(gson.toJson(logEntry) + "\n");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void showHistory() {
        try (FileReader reader = new FileReader(logPath)) {
            Type listType = new TypeToken<ArrayList<Map<String, String>>>() {}.getType();
            List<Map<String, String>> logEntries = gson.fromJson(reader, listType);
            for (Map<String, String> entry : logEntries) {
                System.out.println(entry.get("timestamp") + " - " + entry.get("command"));
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
