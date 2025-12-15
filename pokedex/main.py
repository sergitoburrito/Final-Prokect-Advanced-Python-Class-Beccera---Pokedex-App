from core import PokedexCore


def print_menu():
    print("\n=== Pokédex (Terminal Test) ===")
    print("1) Search Pokémon by name/id")
    print("2) View Favorites")
    print("3) Remove Favorite")
    print("q) Quit")


def main():
    core = PokedexCore()
    print("Pokédex (Terminal Test) — GUI will be added later.")
    print("Favorites loaded:", core.favorites)

    while True:
        print_menu()
        choice = input("Choose an option: ").strip().lower()

        if choice in {"q", "quit", "exit"}:
            break

        
        if choice == "1":
            q = input("Search Pokémon name or id: ").strip()
            p = core.search(q)
            if not p:
                print("Not found (or no internet). Try another name/id.")
                continue

            print(p.short_summary())
            print(p.height_weight_str())


            
            if core.is_favorite(p.name):
                action = input("This is already a favorite. Remove it? (y/n): ").strip().lower()
                if action == "y":
                    core.remove_favorite(p.name)
                    print("Removed. Favorites:", core.list_favorites())
            else:
                action = input("Add to favorites? (y/n): ").strip().lower()
                if action == "y":
                    core.add_favorite(p.name)
                    print("Added. Favorites:", core.list_favorites())

        
        elif choice == "2":
            favs = core.list_favorites()
            if not favs:
                print("No favorites yet.")
            else:
                print("Favorites:")
                for i, name in enumerate(favs, start=1):
                    print(f"  {i}. {name}")

                
                load_choice = input("Type a favorite name to load it (or press Enter to skip): ").strip()
                if load_choice:
                    p = core.search(load_choice)
                    if not p:
                        print("Could not load that favorite (try exact name).")
                    else:
                        print(p.short_summary())

        
        elif choice == "3":
            favs = core.list_favorites()
            if not favs:
                print("No favorites to remove.")
                continue

            print("Favorites:")
            for i, name in enumerate(favs, start=1):
                print(f"  {i}. {name}")

            target = input("Type the name OR number to remove: ").strip()

            
            if target.isdigit():
                idx = int(target)
                if 1 <= idx <= len(favs):
                    name = favs[idx - 1]
                    core.remove_favorite(name)
                    print(f"Removed {name}. Favorites now:", core.list_favorites())
                else:
                    print("Invalid number.")
            else:
                
                if core.is_favorite(target):
                    core.remove_favorite(target)
                    print(f"Removed {target.title()}. Favorites now:", core.list_favorites())
                else:
                    print("That name is not in favorites.")

        else:
            print("Invalid option. Choose 1, 2, 3, or q.")


if __name__ == "__main__":
    main()
