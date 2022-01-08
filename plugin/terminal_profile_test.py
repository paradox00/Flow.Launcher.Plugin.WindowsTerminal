import terminal_profiles

def test():
    profiles = terminal_profiles.TerminalProfiles()
    print(list(profiles.find_installation()))

    print(list(profiles.find_profiles()))

if __name__ == "__main__":
    test()