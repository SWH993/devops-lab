import pandas as pd

# Sample log data for a server
log_data = {
    "timestamp": [
        "2026-03-24 10:00",
        "2026-03-24 10:05",
        "2026-03-24 10:10",
        "2026-03-24 10:15",
    ],
    "cpu_usage": [45, 82, 15, 90],
    "ram_usage_gb": [4, 8, 2, 12],
    "status": ["Online", "Online", "Offline", "Online"],
}

# Creating a DataFrame from the log data
df = pd.DataFrame(log_data)

# Adding a new column to show that server is overloaded
df["is_overloaded"] = df["cpu_usage"] > 80

df["show_offline"] = df["status"] == "Offline"


def analyze_logs():
    print("Server Log Data:")
    print(df)
    print("\nSummary Statistics:")
    print(df.describe())
    print("\nOverloaded Servers:")
    print(df[df["is_overloaded"]])
    print("\nOffline Servers:")
    print(df[df["show_offline"]])


if __name__ == "__main__":
    analyze_logs()
