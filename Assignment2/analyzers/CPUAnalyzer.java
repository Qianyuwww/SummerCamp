package spec.harness.analyzer;

import com.sun.management.OperatingSystemMXBean;
import java.io.*;
import java.lang.management.ManagementFactory;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.ArrayList;
import java.util.List;

public class CPUAnalyzer extends AnalyzerBase {
    private static final OperatingSystemMXBean osBean =
            (OperatingSystemMXBean) ManagementFactory.getOperatingSystemMXBean();
    private static FileWriter writer;
    private static final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");

    public CPUAnalyzer() {
        super();
        try {
            writer = new FileWriter("/home/czh/wd/Summercampus/build/release/SPECjvm2008/cpu_monitor.log", true);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void setup() {
        try {
            writer.write("[" + sdf.format(new Date()) + "] Starting " + getName() + " for " + getBenchmarkName() + "\n");
            writer.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void execute(long time) {
        try {
            double cpuUsage = osBean.getProcessCpuLoad() * 100; // Java 进程 CPU 使用率
            String cpuFreq = getCpuFrequency(); // CPU 频率
            String cacheMisses = getCacheMissRate(); // 缓存未命中率

            writer.write("[" + sdf.format(new Date()) + "] CPU Metrics for " + getBenchmarkName() + ":\n");
            if (cpuUsage >= 0) {
                writer.write("  Process CPU Usage: " + String.format("%.2f", cpuUsage) + "%\n");
            }
            writer.write("  CPU Frequency: " + cpuFreq + "\n");
            writer.write("  Cache Misses: " + cacheMisses + "\n");
            writer.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void tearDown() {
        try {
            writer.write("[" + sdf.format(new Date()) + "] Ending " + getName() + " for " + getBenchmarkName() + "\n");
            writer.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public String getName() {
        return "CPUAnalyzer";
    }

    public static void tearDownAnalyzerClass() {
        try {
            if (writer != null) {
                writer.close();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private String getCpuFrequency() {
        BufferedReader br = null;
        try {
            br = new BufferedReader(new FileReader("/proc/cpuinfo"));
            int coreCount = 36;
            double totalFrequency = 0;

            String line;
            while ((line = br.readLine()) != null) {
                if (line.contains("cpu MHz")) {
                    String[] parts = line.split(":");
                    double frequencyGHz = Double.parseDouble(parts[1].trim()) / 1000;
                    totalFrequency += frequencyGHz;
                }
            }

            if (coreCount > 0) {
                double avgFrequency = totalFrequency / coreCount;
                return String.format("%.2f GHz", avgFrequency);
            }
            return "N/A";
        } catch (Exception e) {
            return "Error: " + e.getMessage();
        } finally {
            if (br != null) {
                try {
                    br.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    private String getCacheMissRate() {
        try {
            String pid = getPid();
            Process process = Runtime.getRuntime().exec("sudo perf stat -e cache-misses,cache-references -p " + pid + " sleep 1");
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getErrorStream()));
            StringBuilder output = new StringBuilder();
            long cacheMisses = 0;
            long cacheReferences = 0;
            String line;
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
                if (line.contains("cache-misses")) {
                    cacheMisses = Long.parseLong(line.trim().split("\\s+")[0].replace(",", ""));
                } else if (line.contains("cache-references")) {
                    cacheReferences = Long.parseLong(line.trim().split("\\s+")[0].replace(",", ""));
                }
            }
            reader.close();
            if (cacheReferences > 0) {
                double missRate = (double) cacheMisses / cacheReferences * 100;
                return String.format("Miss Rate: %.2f%%, Misses: %d, References: %d", missRate, cacheMisses, cacheReferences);
            }
            System.err.println("perf output: " + output.toString());
            return "N/A";
        } catch (IOException e) {
            return "Error: " + e.getMessage();
        } catch (NumberFormatException e) {
            return "Error: Invalid cache metrics format";
        }
    }

    private String getPid() {
        String name = ManagementFactory.getRuntimeMXBean().getName();
        return name.split("@")[0];
    }
}
