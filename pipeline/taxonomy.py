"""Controlled vocabularies: regions, families, countries (ISO2 + continent), sacred-dance cues."""
import re
from .common import norm

REGIONS = ["Africa", "Middle East", "Europe", "Caribbean", "North America", "Central America", "South America",
           "South Asia", "East Asia", "Southeast Asia", "Central Asia", "Oceania", "Global"]

FAMILIES = {
    "classical-court": "Classical & court",
    "folk-circle": "Folk & circle",
    "latin-caribbean": "Latin & Caribbean",
    "african-diaspora": "African & diaspora",
    "street-urban": "Street & urban",
    "ballroom-partner": "Ballroom & partner",
    "ritual-sacred": "Ritual & sacred",
    "stage-contemporary": "Stage & contemporary",
}

# name -> (ISO2, region)
COUNTRIES = {
 "afghanistan":("AF","Central Asia"),"albania":("AL","Europe"),"algeria":("DZ","Africa"),"andorra":("AD","Europe"),"angola":("AO","Africa"),
 "antigua and barbuda":("AG","Caribbean"),"argentina":("AR","South America"),"armenia":("AM","Middle East"),"australia":("AU","Oceania"),"austria":("AT","Europe"),
 "azerbaijan":("AZ","Middle East"),"bahamas":("BS","Caribbean"),"bahrain":("BH","Middle East"),"bangladesh":("BD","South Asia"),"barbados":("BB","Caribbean"),
 "belarus":("BY","Europe"),"belgium":("BE","Europe"),"belize":("BZ","Central America"),"benin":("BJ","Africa"),"bhutan":("BT","South Asia"),
 "bolivia":("BO","South America"),"bosnia and herzegovina":("BA","Europe"),"botswana":("BW","Africa"),"brazil":("BR","South America"),"brunei":("BN","Southeast Asia"),
 "bulgaria":("BG","Europe"),"burkina faso":("BF","Africa"),"burundi":("BI","Africa"),"cambodia":("KH","Southeast Asia"),"cameroon":("CM","Africa"),
 "canada":("CA","North America"),"cape verde":("CV","Africa"),"cabo verde":("CV","Africa"),"central african republic":("CF","Africa"),"chad":("TD","Africa"),
 "chile":("CL","South America"),"china":("CN","East Asia"),"colombia":("CO","South America"),"comoros":("KM","Africa"),"congo":("CG","Africa"),
 "democratic republic of the congo":("CD","Africa"),"dr congo":("CD","Africa"),"costa rica":("CR","Central America"),"croatia":("HR","Europe"),"cuba":("CU","Caribbean"),
 "cyprus":("CY","Europe"),"czech republic":("CZ","Europe"),"czechia":("CZ","Europe"),"denmark":("DK","Europe"),"djibouti":("DJ","Africa"),
 "dominica":("DM","Caribbean"),"dominican republic":("DO","Caribbean"),"ecuador":("EC","South America"),"egypt":("EG","Middle East"),"el salvador":("SV","Central America"),
 "equatorial guinea":("GQ","Africa"),"eritrea":("ER","Africa"),"estonia":("EE","Europe"),"eswatini":("SZ","Africa"),"swaziland":("SZ","Africa"),
 "ethiopia":("ET","Africa"),"fiji":("FJ","Oceania"),"finland":("FI","Europe"),"france":("FR","Europe"),"gabon":("GA","Africa"),
 "gambia":("GM","Africa"),"georgia":("GE","Middle East"),"germany":("DE","Europe"),"ghana":("GH","Africa"),"greece":("GR","Europe"),
 "grenada":("GD","Caribbean"),"guatemala":("GT","Central America"),"guinea":("GN","Africa"),"guinea-bissau":("GW","Africa"),"guyana":("GY","South America"),
 "haiti":("HT","Caribbean"),"honduras":("HN","Central America"),"hungary":("HU","Europe"),"iceland":("IS","Europe"),"india":("IN","South Asia"),
 "indonesia":("ID","Southeast Asia"),"iran":("IR","Middle East"),"iraq":("IQ","Middle East"),"ireland":("IE","Europe"),"israel":("IL","Middle East"),
 "italy":("IT","Europe"),"ivory coast":("CI","Africa"),"cote d'ivoire":("CI","Africa"),"jamaica":("JM","Caribbean"),"japan":("JP","East Asia"),
 "jordan":("JO","Middle East"),"kazakhstan":("KZ","Central Asia"),"kenya":("KE","Africa"),"kiribati":("KI","Oceania"),"kosovo":("XK","Europe"),
 "kuwait":("KW","Middle East"),"kyrgyzstan":("KG","Central Asia"),"laos":("LA","Southeast Asia"),"latvia":("LV","Europe"),"lebanon":("LB","Middle East"),
 "lesotho":("LS","Africa"),"liberia":("LR","Africa"),"libya":("LY","Middle East"),"liechtenstein":("LI","Europe"),"lithuania":("LT","Europe"),
 "luxembourg":("LU","Europe"),"madagascar":("MG","Africa"),"malawi":("MW","Africa"),"malaysia":("MY","Southeast Asia"),"maldives":("MV","South Asia"),
 "mali":("ML","Africa"),"malta":("MT","Europe"),"marshall islands":("MH","Oceania"),"mauritania":("MR","Africa"),"mauritius":("MU","Africa"),
 "mexico":("MX","North America"),"micronesia":("FM","Oceania"),"moldova":("MD","Europe"),"monaco":("MC","Europe"),"mongolia":("MN","East Asia"),
 "montenegro":("ME","Europe"),"morocco":("MA","Africa"),"mozambique":("MZ","Africa"),"myanmar":("MM","Southeast Asia"),"burma":("MM","Southeast Asia"),
 "namibia":("NA","Africa"),"nauru":("NR","Oceania"),"nepal":("NP","South Asia"),"netherlands":("NL","Europe"),"new zealand":("NZ","Oceania"),
 "nicaragua":("NI","Central America"),"niger":("NE","Africa"),"nigeria":("NG","Africa"),"north korea":("KP","East Asia"),"north macedonia":("MK","Europe"),
 "macedonia":("MK","Europe"),"norway":("NO","Europe"),"oman":("OM","Middle East"),"pakistan":("PK","South Asia"),"palau":("PW","Oceania"),
 "palestine":("PS","Middle East"),"panama":("PA","Central America"),"papua new guinea":("PG","Oceania"),"paraguay":("PY","South America"),"peru":("PE","South America"),
 "philippines":("PH","Southeast Asia"),"poland":("PL","Europe"),"portugal":("PT","Europe"),"qatar":("QA","Middle East"),"romania":("RO","Europe"),
 "russia":("RU","Europe"),"rwanda":("RW","Africa"),"saint kitts and nevis":("KN","Caribbean"),"saint lucia":("LC","Caribbean"),"saint vincent and the grenadines":("VC","Caribbean"),
 "samoa":("WS","Oceania"),"san marino":("SM","Europe"),"sao tome and principe":("ST","Africa"),"saudi arabia":("SA","Middle East"),"senegal":("SN","Africa"),
 "serbia":("RS","Europe"),"seychelles":("SC","Africa"),"sierra leone":("SL","Africa"),"singapore":("SG","Southeast Asia"),"slovakia":("SK","Europe"),
 "slovenia":("SI","Europe"),"solomon islands":("SB","Oceania"),"somalia":("SO","Africa"),"south africa":("ZA","Africa"),"south korea":("KR","East Asia"),
 "korea":("KR","East Asia"),"south sudan":("SS","Africa"),"spain":("ES","Europe"),"sri lanka":("LK","South Asia"),"sudan":("SD","Africa"),
 "suriname":("SR","South America"),"sweden":("SE","Europe"),"switzerland":("CH","Europe"),"syria":("SY","Middle East"),"taiwan":("TW","East Asia"),
 "tajikistan":("TJ","Central Asia"),"tanzania":("TZ","Africa"),"thailand":("TH","Southeast Asia"),"timor-leste":("TL","Southeast Asia"),"east timor":("TL","Southeast Asia"),
 "togo":("TG","Africa"),"tonga":("TO","Oceania"),"trinidad and tobago":("TT","Caribbean"),"tunisia":("TN","Africa"),"turkey":("TR","Middle East"),
 "turkiye":("TR","Middle East"),"turkmenistan":("TM","Central Asia"),"tuvalu":("TV","Oceania"),"uganda":("UG","Africa"),"ukraine":("UA","Europe"),
 "united arab emirates":("AE","Middle East"),"united kingdom":("GB","Europe"),"uk":("GB","Europe"),"england":("GB","Europe"),"scotland":("GB","Europe"),
 "wales":("GB","Europe"),"northern ireland":("GB","Europe"),"united states":("US","North America"),"usa":("US","North America"),"united states of america":("US","North America"),
 "uruguay":("UY","South America"),"uzbekistan":("UZ","Central Asia"),"vanuatu":("VU","Oceania"),"venezuela":("VE","South America"),"vietnam":("VN","Southeast Asia"),
 "yemen":("YE","Middle East"),"zambia":("ZM","Africa"),"zimbabwe":("ZW","Africa"),"puerto rico":("PR","Caribbean"),"hong kong":("HK","East Asia"),
 "macau":("MO","East Asia"),"tibet":("CN","East Asia"),"hawaii":("US","Oceania"),"tahiti":("PF","Oceania"),"french polynesia":("PF","Oceania"),
 "cook islands":("CK","Oceania"),"new caledonia":("NC","Oceania"),"guam":("GU","Oceania"),"greenland":("GL","North America"),"reunion":("RE","Africa"),
 "martinique":("MQ","Caribbean"),"guadeloupe":("GP","Caribbean"),"curacao":("CW","Caribbean"),"aruba":("AW","Caribbean"),"bermuda":("BM","North America"),
 "cayman islands":("KY","Caribbean"),"faroe islands":("FO","Europe"),"western sahara":("EH","Africa"),"basque country":("ES","Europe"),"catalonia":("ES","Europe"),
}

COUNTRIES_N = {norm(k): v for k, v in COUNTRIES.items()}

def country_lookup(name):
    """Return (iso2, region) or (None, None). Accepts 'Lebanon, Syria' / 'Argentina and Uruguay' (first match wins)."""
    raw = str(name or "")
    if not raw.strip():
        return None, None
    parts = [raw] + [p for p in re.split(r",|/|;|\band\b|&", raw) if p.strip()]
    for part in parts:
        n = norm(part)
        if not n:
            continue
        if n in COUNTRIES_N:
            return COUNTRIES_N[n]
        for pref in ("the ", "republic of ", "kingdom of ", "state of ", "federal republic of ", "people s republic of "):
            if n.startswith(pref) and n[len(pref):] in COUNTRIES_N:
                return COUNTRIES_N[n[len(pref):]]
    return None, None

ISO_TO_REGION = {v[0]: v[1] for v in COUNTRIES.values()}

SACRED_CUES = ["ritual", "sacred", "ceremon", "temple", "shaman", "trance", "possession", "deity", "deities", "god", "goddess",
               "worship", "prayer", "liturg", "exorcis", "initiation", "funeral", "ancestor", "spirit", "sufi", "dervish",
               "religious", "devotional", "purification", "offering", "monastery", "monk", "priest"]

def sacred_hint(text):
    t = norm(text)
    hits = [c for c in SACRED_CUES if c in t]
    return len(hits) >= 2, hits
