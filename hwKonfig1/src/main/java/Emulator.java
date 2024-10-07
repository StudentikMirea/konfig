import java.util.Scanner;

public class Emulator {
    public static void main(String[] args) {
        Config config = new Config("config.ini");
        if (config.getVfsPath() == null || config.getLogPath() == null) {
            System.out.println("Configuration file not found or incorrect.");
            return;
        }

        VirtualFileSystem vfs = new VirtualFileSystem(config.getVfsPath());
        Logger logger = new Logger(config.getLogPath());

        Scanner scanner = new Scanner(System.in);
        String hostname = config.getHostname();

        while (true) {
            System.out.print(hostname + ":" + vfs.getCurrentDir() + "$ ");
            String command = scanner.nextLine();
            logger.logAction(command);

            if (command.startsWith("ls")) {
                System.out.println(vfs.ls());
            } else if (command.startsWith("cd")) {
                String[] parts = command.split(" ", 2);
                if (parts.length == 2) {
                    vfs.cd(parts[1]);
                }
            } else if (command.equals("exit")) {
                vfs.exit();
                break;
            } else if (command.equals("uname")) {
                System.out.println(vfs.uname());
            } else if (command.startsWith("tac")) {
                String[] parts = command.split(" ", 2);
                if (parts.length == 2) {
                    vfs.tac(parts[1]);
                }
            } else if (command.equals("history")) {
                logger.showHistory();
            } else {
                System.out.println("Unknown command");
            }
        }
    }
}
