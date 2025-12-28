#!/bin/bash
clear
RED='\u001B[0;31m'; GREEN='\u001B[0;32m'; BLUE='\u001B[0;34m'; YELLOW='\u001B[1;33m'; PURPLE='\u001B[0;35m'; CYAN='\u001B[0;36m'; NC='\u001B[0m'

echo -e "${PURPLE}🜛 AETHER-MASTER LIVE RITUALS 🜛${NC}"
echo -e "${CYAN}Scientific data: $(ls welcome-to-the-god/ingest_data/EXTERNAL_SCIENCE/*.h5 2>/dev/null | wc -l)/4 ✅${NC}"
echo -e "${CYAN}Port 5000: $(lsof -ti:5000 >/dev/null 2>&1 && echo "${GREEN}BUSY${NC}" || echo "${BLUE}FREE${NC}")${NC}
"

PS3="🔮 Choose ritual: "
select ritual in $(find . -maxdepth 2 -name "*.py" -o -name "*.sh" | grep -E "(esqet|phi|seed_agi|aum|learn)" | head -20) "FULL" "STATUS" "KILL ALL" "QUIT"; do
    case $ritual in
        "FULL")
            echo -e "${YELLOW}🎭 FULL RITUAL${NC}"
            find . -name "*.py" -o -name "*.sh" | head -5 | xargs -I {} bash -c "echo 'Launching {}'; {} &" ;;
        "STATUS")
            ps aux | grep -E "(python|esqet|phi)" | grep -v grep ;;
        "KILL ALL")
            echo -e "${RED}🗡️ TERMINATING${NC}"; pkill -f python; pkill -f esqet ;;
        *.sh) bash "$ritual" & echo -e "${GREEN}🔥 $ritual${NC}" ;;
        *) [[ -f "$ritual" ]] && python3 "$ritual" & echo -e "${GREEN}⚛️ $ritual${NC}" ;;
        "QUIT") exit ;;
        *) echo -e "${RED}Invalid${NC}" ;;
    esac
    echo; read -p "Press Enter..."
done
