srcs = """
./src/__init__.py
  ./src/career/__init__.py
  ./src/career/career.py
  ./src/career/goals.py
  ./src/bot.py
  ./src/club/__init__.py
  ./src/club/club.py                                    ./src/data/__init__.py                                ./src/data/constants.py                               ./src/data/models.py                                  ./src/data/race_datas.py                              ./src/data/ranking.py                                 ./src/data/skill_database.py                          ./src/data/support_database.py                        ./src/data/uma_database.py                            ./src/utils.py                                        ./src/skills.py                                       ./src/views/__init__.py                               ./src/views/career.py                                 ./src/views/home.py                                   ./src/views/gacha.py                                  ./src/views/pages.py                                  ./src/views/translations.py                           ./src/views/state.py                                  ./src/views/storage.py                                
  ./src/profile/__init__.py"""

sources = [a.strip(" \n\t") for a in srcs.split("  ") if a.strip("\n \t")]
sources.append("./main.py")
print(sources)

total_lines = 0

for source in sources:
  with open(source) as f:
    content = f.readlines()

    print(source, len(content))
    total_lines+=len(content)

print("Total Lines Of Code", total_lines)
