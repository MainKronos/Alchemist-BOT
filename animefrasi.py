import json
from bs4 import BeautifulSoup
import requests

HDR = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36'}



def main():

	links = [
		"https://www.animefeels.it/a-place-further-than-the-universe/",
		"https://www.animefeels.it/after-the-rain/",
		"https://www.animefeels.it/aggretsuko/",
		"https://www.animefeels.it/akagami-no-shirayuki-hime/",
		"https://www.animefeels.it/akame-ga-kill/",
		"https://www.animefeels.it/amnesia/",
		"https://www.animefeels.it/angel-beats/",
		"https://www.animefeels.it/angel-sanctuary/",
		"https://www.animefeels.it/ano-hana/",
		"https://www.animefeels.it/ano-hana-movie/",
		"https://www.animefeels.it/ano-natsu-de-matteru/",
		"https://www.animefeels.it/anonymous-noise/",
		"https://www.animefeels.it/another/",
		"https://www.animefeels.it/ao-haru-ride/",
		"https://www.animefeels.it/arakawa-under-the-bridge/",
		"https://www.animefeels.it/arte/",
		"https://www.animefeels.it/assassination-classroom/",
		"https://www.animefeels.it/attack-on-titan/",
		"https://www.animefeels.it/attack-on-titan-terza-stagione/",
		"https://www.animefeels.it/baccano/",
		"https://www.animefeels.it/bakemonogatari/",
		"https://www.animefeels.it/bakuman/",
		"https://www.animefeels.it/banana-fish/",
		"https://www.animefeels.it/barakamon/",
		"https://www.animefeels.it/beastars/",
		"https://www.animefeels.it/beelzebub/",
		"https://www.animefeels.it/berserk/",
		"https://www.animefeels.it/binbougami-ga/",
		"https://www.animefeels.it/black-bullet/",
		"https://www.animefeels.it/black-clover/"
		"https://www.animefeels.it/black-lagoon/",
		"https://www.animefeels.it/bleach/",
		"https://www.animefeels.it/bleach-manga/",
		"https://www.animefeels.it/blood-lad/",
		"https://www.animefeels.it/blue-exorcist/",
		"https://www.animefeels.it/boku-wa-tomodachi-ga-sukunai/",
		"https://www.animefeels.it/bokura-ga-ita/",
		"https://www.animefeels.it/bokura-wa-minna-kawaisou/",
		"https://www.animefeels.it/bungo-stray-dogs/",
		"https://www.animefeels.it/carole-and-tuesday/",
		"https://www.animefeels.it/cells-at-works/",
		"https://www.animefeels.it/chaos-head/",
		"https://www.animefeels.it/charlotte/",
		"https://www.animefeels.it/chihayafuru/",
		"https://www.animefeels.it/chuunibyou-demo-koi-ga-shitai/",
		"https://www.animefeels.it/clannad/",
		"https://www.animefeels.it/claymore/",
		"https://www.animefeels.it/code-geass/",
		"https://www.animefeels.it/code-geass/",
		"https://www.animefeels.it/cowboy-bebop/",
		"https://www.animefeels.it/d-gray-man/",
		"https://www.animefeels.it/danganronpa-the-animation/",
		"https://www.animefeels.it/darker-than-black/",
		"https://www.animefeels.it/darling-in-the-franxx/",
		"https://www.animefeels.it/deadman-wonderland/",
		"https://www.animefeels.it/death-note/",
		"https://www.animefeels.it/death-parade/",
		"https://www.animefeels.it/demon-slayer/",
		"https://www.animefeels.it/devilman-crybaby/",
		"https://www.animefeels.it/dororo/",
		"https://www.animefeels.it/dr-stone/",
		"https://www.animefeels.it/durarara/",
		"https://www.animefeels.it/elfen-lied/",
		"https://www.animefeels.it/erased/",
		"https://www.animefeels.it/ergo-proxy/",
		"https://www.animefeels.it/eureka-seven/",
		"https://www.animefeels.it/fairy-tail/",
		"https://www.animefeels.it/fate-stay-night/",
		"https://www.animefeels.it/food-wars/",
		"https://www.animefeels.it/free/",
		"https://www.animefeels.it/fruits-basket/",
		"https://www.animefeels.it/fruits-basket-2019/",
		"https://www.animefeels.it/full-metal-panic/",
		"https://www.animefeels.it/fullmetal-alchemist-brotherhood/",
		"https://www.animefeels.it/gekkan-shoujo-nozaki-kun/",
		"https://www.animefeels.it/gintama-serie-italiana/",
		"https://www.animefeels.it/gintama/",
		"https://www.animefeels.it/gintama-2011/",
		"https://www.animefeels.it/gintama-2017/",
		"https://www.animefeels.it/given/",
		"https://www.animefeels.it/gokukoku-no-brynhildr/",
		"https://www.animefeels.it/golden-time/",
		"https://www.animefeels.it/great-teacher-onizuka/",
		"https://www.animefeels.it/grisaia-no-kajitsu/",
		"https://www.animefeels.it/gugure-kokkuri-san/",
		"https://www.animefeels.it/guilty-crown/",
		"https://www.animefeels.it/haikyuu/",
		"https://www.animefeels.it/hanamonogatari/",
		"https://www.animefeels.it/hataraku-maou-sama/",
		"https://www.animefeels.it/highschool-dxd/",
		"https://www.animefeels.it/highschool-of-the-dead/",
		"https://www.animefeels.it/higurashi-no-naku-koro-ni/",
		"https://www.animefeels.it/himouto-umaru-chan/",
		"https://www.animefeels.it/honey-and-clover/",
		"https://www.animefeels.it/hoozuki-no-reitetsu/",
		"https://www.animefeels.it/host-club/",
		"https://www.animefeels.it/hotarubi-no-mori-e/",
		"https://www.animefeels.it/hunter-x-hunter/",
		"https://www.animefeels.it/hyouka/",
		"https://www.animefeels.it/i-cavalieri-dello-zodiaco/",
		"https://www.animefeels.it/il-castello-errante-di-howl/",
		"https://www.animefeels.it/il-giardino-delle-parole/",
		"https://www.animefeels.it/inu-x-boku-ss/",
		"https://www.animefeels.it/inuyasha/",
		"https://www.animefeels.it/irozuku-sekai-no-ashita-kara/",
		"https://www.animefeels.it/jibaku-shonen-hanako-kun/",
		"https://www.animefeels.it/jojo-s-bizzarre-adventures/",
		"https://www.animefeels.it/k-on/",
		"https://www.animefeels.it/kaguya-sama-love-is-war/",
		"https://www.animefeels.it/kaichou-wa-maid-sama/",
		"https://www.animefeels.it/kamisama-hajimemashita/",
		"https://www.animefeels.it/kill-la-kill/",
		"https://www.animefeels.it/kimi-ni-todoke/",
		"https://www.animefeels.it/kimi-no-na-wa-your-name/",
		"https://www.animefeels.it/kiseiju/",
		"https://www.animefeels.it/koe-no-katachi-a-silent-voice/",
		"https://www.animefeels.it/koi-to-uso/",
		"https://www.animefeels.it/konosuba/",
		"https://www.animefeels.it/koutetsujou-no-kabaneri/",
		"https://www.animefeels.it/kuroko-no-basket/",
		"https://www.animefeels.it/kuroshitsuji/",
		"https://www.animefeels.it/kuroshitsuji-book-of-circus/",
		"https://www.animefeels.it/kuzu-no-honkai/",
		"https://www.animefeels.it/kyoukai-no-kanata/",
		"https://www.animefeels.it/la-malinconia-di-haruhi-suzumiya/",
		"https://www.animefeels.it/le-situazioni-di-lui-e-di-lei/",
		"https://www.animefeels.it/little-busters/",
		"https://www.animefeels.it/lovely-complex/",
		"https://www.animefeels.it/made-in-abyss/",
		"https://www.animefeels.it/magi-the-labyrinth-of-magic/",
		"https://www.animefeels.it/maquia/",
		"https://www.animefeels.it/march-comes-in-like-a-lion/",
		"https://www.animefeels.it/mawaru-penguindrum/",
		"https://www.animefeels.it/mekakucity-actors/",
		"https://www.animefeels.it/mirai-nikki/",
		"https://www.animefeels.it/miyo-un-amore-felino/",
		"https://www.animefeels.it/monogatari-series-second-season/",
		"https://www.animefeels.it/mushishi/",
		"https://www.animefeels.it/my-hero-academia/",
		"https://www.animefeels.it/my-little-monster/",
		"https://www.animefeels.it/nabari/",
		"https://www.animefeels.it/nagi-no-asukara/",
		"https://www.animefeels.it/nana/",
		"https://www.animefeels.it/naruto/",
		"https://www.animefeels.it/naruto-shippuden/",
		"https://www.animefeels.it/natsume-yuujinchou/",
		"https://www.animefeels.it/nekomonogatari/",
		"https://www.animefeels.it/neon-genesis-evangelion/",
		"https://www.animefeels.it/nier-automata/",
		"https://www.animefeels.it/nisekoi/",
		"https://www.animefeels.it/nisemonogatari/",
		"https://www.animefeels.it/no-game-no-life/",
		"https://www.animefeels.it/no-6/",
		"https://www.animefeels.it/noragami/",
		"https://www.animefeels.it/noucome/",
		"https://www.animefeels.it/oltre-le-nuvole/",
		"https://www.animefeels.it/one-piece/",
		"https://www.animefeels.it/one-punch-man/",
		"https://www.animefeels.it/orange/",
		"https://www.animefeels.it/ore-monogatari/",
		"https://www.animefeels.it/owari-no-seraph/",
		"https://www.animefeels.it/owarimonogatari/",
		"https://www.animefeels.it/pandora-hearts/",
		"https://www.animefeels.it/plastic-memories/",
		"https://www.animefeels.it/prison-school/",
		"https://www.animefeels.it/psycho-pass/",
		"https://www.animefeels.it/puella-magi-madoka-magica/",
		"https://www.animefeels.it/puella-magi-madoka-magica-movie-3-rebellion/",
		"https://www.animefeels.it/quando-c-era-marnie/",
		"https://www.animefeels.it/re-zero/",
		"https://www.animefeels.it/relife/",
		"https://www.animefeels.it/romeo-x-juliet/",
		"https://www.animefeels.it/rossana/",
		"https://www.animefeels.it/sailor-moon/",
		"https://www.animefeels.it/saiyuki/",
		"https://www.animefeels.it/sakurasou-no-pet-na-kanojo/",
		"https://www.animefeels.it/samurai-champloo/",
		"https://www.animefeels.it/say-i-love-you/",
		"https://www.animefeels.it/shigatsu-wa-kimi-no-uso/",
		"https://www.animefeels.it/shimoneta/",
		"https://www.animefeels.it/shinsekai-yori/",
		"https://www.animefeels.it/showa-genroku-rakugo-shinju/",
		"https://www.animefeels.it/silver-spoon/",
		"https://www.animefeels.it/sket-dance/",
		"https://www.animefeels.it/somali-and-the-forest-spirit/",
		"https://www.animefeels.it/soredemo-sekai-wa-utsukushi/",
		"https://www.animefeels.it/soul-eater/",
		"https://www.animefeels.it/special-a/",
		"https://www.animefeels.it/spice-and-wolf/",
		"https://www.animefeels.it/steins-gate/",
		"https://www.animefeels.it/steins-gate-0/",
		"https://www.animefeels.it/sword-art-online/",
		"https://www.animefeels.it/tengen-toppa-gurren-lagann/",
		"https://www.animefeels.it/the-ancient-magus-bride/",
		"https://www.animefeels.it/the-promised-neverland/",
		"https://www.animefeels.it/the-rising-of-the-shield-hero/",
		"https://www.animefeels.it/the-seven-deadly-sins/",
		"https://www.animefeels.it/the-world-god-only-knows/",
		"https://www.animefeels.it/tokyo-ghoul/",
		"https://www.animefeels.it/tokyo-ghoul-re/",
		"https://www.animefeels.it/tokyo-magnitude-8-0/",
		"https://www.animefeels.it/toradora/",
		"https://www.animefeels.it/tower-of-god/",
		"https://www.animefeels.it/tutor-hitman-reborn/",
		"https://www.animefeels.it/vampire-knight/",
		"https://www.animefeels.it/violet-evergarden/",
		"https://www.animefeels.it/voglio-mangiare-il-tuo-pancreas/",
		"https://www.animefeels.it/watamote/",
		"https://www.animefeels.it/weathering-with-you/",
		"https://www.animefeels.it/welcome-to-nhk/",
		"https://www.animefeels.it/wolf-children/",
		"https://www.animefeels.it/wolf-girl-and-black-prince/",
		"https://www.animefeels.it/xxxholic/",
		"https://www.animefeels.it/yahari-ore-no-seishun-lovecome-wa-machigatte-iru/",
		"https://www.animefeels.it/yuri-on-ice/",
		"https://www.animefeels.it/zankyou-no-terror/",
		"https://www.animefeels.it/zero-no-tsukaima/",
		"https://www.animefeels.it/zetsuen-no-tempest/",
		"https://www.animefeels.it/5-cm-al-secondo/",
		"https://www.animefeels.it/91-days/"
	]

	for link in links:
		print(link.replace("https://www.animefeels.it/", "").replace("/", "").replace("-", " "))

	# getFrasi(links)

def getFrasi(links):

	animeFrasi = []

	# f=open("animeFrasi.json", 'r')
	# animeFrasi = json.loads(f.read())
	# f.close()


	for link in links:

		sb_get = requests.get(link, headers = HDR)
		soupeddata = BeautifulSoup(sb_get.content, "html.parser")


		blocks = soupeddata.find_all("div", { "class" : "vc_col-sm-12 wpb_column column_container vc_column_container col padding-2-percent" })

		for block in blocks:
			rawTXT= block.find_all("span", { "style" : "color: #ffffff;" })

			

			try:
				testo = rawTXT[0].get_text()
				autore = rawTXT[1].get_text()
			except Exception as e:
				pass
			else:
				if {autore:testo} not in animeFrasi:
					animeFrasi.append({autore:testo})

	print(len(animeFrasi))
	f=open("animeFrasi.json", 'w')
	f.write(json.dumps(animeFrasi, indent='\t'))
	f.close()



main()