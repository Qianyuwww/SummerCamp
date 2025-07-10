package spec.harness.analyzer;

import java.lang.management.*;
import java.io.*;
import java.text.SimpleDateFormat;
import java.util.Date;

public class JVMAnalyzer extends AnalyzerBase {
    private static final GarbageCollectorMXBean gcBean =
            ManagementFactory.getGarbageCollectorMXBeans().get(0); // 假设使用第一个 GC
    private static final CompilationMXBean jitBean =
            ManagementFactory.getCompilationMXBean();
    private static final MemoryMXBean memoryBean =
            ManagementFactory.getMemoryMXBean();
    private static FileWriter writer;
    private static final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");

    public JVMAnalyzer() {
        super();
        try {
            writer = new FileWriter("/home/czh/wd/Summercampus/build/release/SPECjvm2008/jvm_monitor.log", true);
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
            long gcCount = gcBean.getCollectionCount();
            long gcTime = gcBean.getCollectionTime();
            long jitTime = jitBean.getTotalCompilationTime();
            MemoryUsage heapUsage = memoryBean.getHeapMemoryUsage();

            writer.write("[" + sdf.format(new Date()) + "] JVM Metrics for " + getBenchmarkName() + ":\n");
            writer.write("  GC Count: " + gcCount + ", GC Time: " + gcTime + " ms\n");
            writer.write("  JIT Compilation Time: " + jitTime + " ms\n");
            writer.write("  Heap Usage: " + heapUsage.getUsed() / (1024 * 1024) + " MB / " +
                         heapUsage.getMax() / (1024 * 1024) + " MB\n");
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
        return "JVMAnalyzer";
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
}
