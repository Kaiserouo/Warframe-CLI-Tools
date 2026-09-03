> ref. src\data\inventory\parse_inventory.py, get_inventory()

# General Information
- `Created`: 創帳時間
- `RewardSeed`: 老實說不確定，好像 browser.wf 有拿來算什麼東西？
- `DuviriInfo`: 跟 duviri 隨機性有關的東西
- `GiftsRemaining`: 剩餘送禮次數
- `TradesRemaining`: s/a
- `Mailbox`: 裡面只有記一個 `LastInboxId`，那個 oid 檔案不存在，在想實際內容或許不在 inventory 裡？
- `SeasonChallengeHistory`: nightwave 的任務，只寫 challenge 名和 id，不知道實際意義
- `StoryModeChoice`: 一個字串，猜想是剛開始的時候是正常遊玩還是先去渡域
- `PlayedParkourTutorial`: bool，沒有很確定
- `QuestKeys`: 關於任務的紀錄，感覺他是靠某種 key item (`Key`, `KeyChain`) 來表示是甚麼任務，然後這個會記錄你有沒有完成，完成時間等等，有奇葩的資料不清楚用途
- `ReceivedStartingGear`: bool，沒有很確定
- `ChallengeProgress`: 進度，含成就頁面的成就 / honoria (`Title`) 相關 / incarnon (`<name>Challenge<alphabet>`) / 在節點的任務 (e.g., `VMStartCraftingRhino`) / 1999 電腦的任務 (`Calendar*`) / Nightwave 的任務 (`Season[Weekly]*`)
- `LastRegionPlayed`: 字串，可能是在星圖要顯示的時候知道上一次玩的圖在哪他好放大？
- `Missions`: 似乎是星圖的點的完成次數，以及... 某個 `Tier` 的 tag，先猜 0 是普通 1 是鋼韌？
- `XPInfo`: 每個甲和武器得到的 affinity，在個人頁面看的到
- `Affiliations`: 各 syndicate 的狀況，等級以及所擁有的聲望
- `CompletedJobs`: 可能是跟 bounty 有關的東西，不確定實際意義
- `LoreFragmentScans`: 物品類的掃描進度
- `Boosters`: 現在有的加倍以及何時失效
- `DiscoveredMarkers`: 沒有很確定，在猜是紀錄有沒有去過開放地圖的某個洞窟的，以整數表記，猜是 bitmap
- `PlayerLevel`: 目前等級 / mastery rank，注意 LR6 的話會記錄 36
- `DeathMarks`: 目前拿到的死亡標記，注意 stalker 會是每個 boss 標記一次
- `EmailItems`: 老實說我沒有很確定，有點像是收件箱但是他只記錄 type 和 count 沒紀錄順序或時間？
- `LoginMilestoneRewards`: 領過的 milestone reward
- `GuildId`: 氏族 ID
- `ActiveDojoColorResearch`: 目前氏族在做的顏色
- `Drones`: Extractor 相關
- `FocusXP`: Focus point，指揮官各學校的 affinity
- `ActiveAvatarImageType`: 目前用的 glyph
- `PlayerSkills`: intrinsics，內蘊
- `OneTimePurchases`: 只能買一次的東西，e.g., Aoi 賣的歌，Prex card，(可能有) scene 等等
- `Wishlist`: 商店 wishlist
- `TitleType`: 目前用的 honoria
- `EvolutionProgress`: incarnon 進化相關進度，是以物品種類為單位紀錄的，i.e., 不用每把同樣的武器都重跑進化
- `BlessingCooldown`: 距離下次 true master's font 可用 (吧，不確定時間本身的意義)


# Warframe Website Information
- `SubscribedToEmails`: 沒意外應該是某種網站上的訂閱
- `SubscribedToEmailsPersonalized`: s/a
- `WebFlags`: 各種跟網站有關的東西，e.g., 有沒有領獎勵，有沒有 / 甚麼時候去過甚麼頁面

# Inventory

## General
- `Consumables`: 消耗品類？有 `ItemCount: int` 和 `ItemType: uname`
- `FlavourItems`: 猜想有關 cosmetic / skins (`Skins`, landing craft, etc) / animation set / emote (`Emotes`) / glyph (`AvatarImages`) / color palette / honoria (`Titles`) / 從黃臉買的小遊戲 (`Arcade`) 應該會在這。因為沒有寫數量，我在猜應該是「本質上一個人就只能有一個 / 獲得一次」的東西都在這
- `RawUpgrades`: 沒有升級的模組 / mod
- `Upgrades`: 有升級的模組 / mod，我猜測如果你裝了沒升級的模組也會放在這裡 (他理論上會需要一個 oid？)，必須實驗
- `WeaponSkins`: warframe 相關的 skin，主要是皮和頭盔，似乎能裝在甲上的都算？以及武器相關的 skin，對沒錯他叫 weapon skin 然後裝一堆甲的東西
- `MiscItems`: 普通資源，rubedo / orokin cell 之類的，猜想應該是能在 inventory 看到的都在這？注意藍圖 (e.g., Voruna Prime Blueprint) 並不會在這裡，會在 `Recipe`
- `Recipes`: 藍圖 / blueprint
- `PendingRecipes`: 現在正在 foundry 做的東西，以及他的完成時間
- `ShipDecorations`: 裝飾品，能擺出來的都算
- `LevelKeys`: 關卡相關的 key，似乎是有那種需要某物品才能打的關卡都在這
- `FusionTreasures`: ayatan sculpture
- `InfestedFoundry`: helminth
- `KubrowPetPrints`: 所有的 imprint 紀錄

## Currency
- `FusionPoints`: endo，內融核心
- `RegularCredits`: credit / hollar，普通的錢
- `PremiumCreditsFree`: free platinum 數量
- `PremiumCredits`: platinum，不知道是不是跟免費的另記 (應該是)
- `PrimeTokens`: 應該是 regal aya

## Loadouts

### Frame / Wings
- `Ships`: landing craft
- `Suits`: warframe
- `SpaceSuits`: archwing
- `MechSuits`: necramech
- `Sentinels`: 機器相關寵物
- `KubrowPets`: 狗相關寵物
- `MoaPets`: 機器狗相關寵物
- `Hoverboards`: K drive
- `AdultOperatorLoadOuts`: drifter 的皮和附能
- `KahlLoadOuts`: kahl 的皮
- `OperatorLoadOuts`: operator 的皮和附能
- `OperatorSuits`: operator 的皮，我猜是真的皮膚相關而非衣服...
- `Horses`: 馬的皮
- `FocusAbility`: 字串，猜想是目前裝的學校
- `FocusUpgrades`: 升級，用專精點數換的那些

### Weapons (general attack weapon)

- `LongGuns`: primary
- `Melee`: melee
- `Pistols`: secondary
- `SpecialItems`: exalted weapon，含 necramech / (沒辦法脫的) 寵物武器 (狗，etc) / Yareli 的板子 / Orion
- `SpaceGuns`: archgun
- `SpaceMelee`: archmelee
- `SentinelWeapons`: companion weapons (注意狗相關的在 `SpecialItems`)
- `Antiques`: tektolyst artifact 模組和皮
- `OperatorAmps`: Amp 相關，皮以及它是XXX

### Railjack
- `CrewShipHarnesses`: 沒意外是 railjack 的模組？
- `CrewShips`: railjack 裝上去的東西，武器，船員，皮
- `CrewMembers`: 船員
- `CrewShipRawSalvage`: 沒碰過的零件 (武器和非武器)
- `CrewShipSalvagedWeaponSkins`: 開過的非武器零件 (shield array, engine, hull, reactor)
- `CrewShipSalvagedWeapons`: 開過的武器
- `CrewShipWeaponSkins`: 目前擁有非武器零件 (shield array, engine, hull, reactor)
- `CrewShipWeapons`: 目前擁有的武器

### Other
- `DataKnives`: Parazon
- `Scoops`: lunaro
- `LoadOutPresets`: 似乎存有每個 loadout 的內容
- `SpectreLoadouts`: spectre 相關
- `EquippedGear`: 目前裝的東西的 uname
- `DrifterMelee`: 感覺主要是 skin 的部分？
- `CurrentLoadOutIds`: 有 11 個 id，應該是目前各使用的 loadout，似乎都在 `LoadoutPresets` 裡面
- `PersonalTechProjects`: 紀錄 railjack 做東西的時候已經給多少材料之類的

## Bin / Slots
基本上都是記個幾個整數這樣
- `CrewMemberBin`: 船員
- `CrewShipSalvageBin`: railjack 相關 
- `MechBin`: necramech
- `OperatorAmpBin`: amp 
- `PveBonusLoadoutBin`: loadout 
- `PvpBonusLoadoutBin`: loadout
- `RandomModBin`: riven
- `SentinelBin`: companion (我猜是所有寵物都算在裡面)
- `SpaceSuitBin`: archwing
- `SpaceWeaponBin`: archgun + archmelee?
- `SuitBin`: warframe
- `WeaponBin`: primary / secondary / melee

# Daily Standing
- `SupportedSyndicate`: 目前選的 syndicate
- `DailyAffiliation`: 應該是那六個 syndicate 的 standing，顯示的數值是今天還有多少沒有領 (並不是今天已經領了多少)
- `DailyAffiliationCavia`: cavia
- `DailyAffiliationCetus`: cetus
- `DailyAffiliationEntrati`: necralisk
- `DailyAffiliationKahl`: kahl's garrison (吧)
- `DailyAffiliationLibrary`: 黃臉 / cephalon simaris
- `DailyAffiliationNecraloid`: necraloid
- `DailyAffiliationPvp`: conclaive
- `DailyAffiliationQuills`: cetus quill
- `DailyAffiliationSolaris`: solaris united
- `DailyAffiliationVentkids`: ventkids
- `DailyAffiliationVox`: vox solaris
- `DailyAffiliationZariman`: holdfast
- `DailyAffiliationHex`: hex
- `DailyFocus`: 指揮官的 focus point

# Archimedea
- `EntratiLabConquestActiveFrameVariants`: 下面四個詞條
- `EntratiLabConquestHardModeStatus`: 你有選擇上面的 EDA 選項嗎？bool
- `EntratiVaultCountResetDate`: 不知道，猜測是換周時間
- `EntratiLabConquestUnlocked`: 有開 EDA 了嗎？bool
- `EntratiVaultCountLastPeriod`: 不知道，目前是數字 5
- `EntratiLabConquestCacheScoreMission`: 這周已經拿到過的分數 (顯示下面的進度條用)

- `EchoesHexConquestActiveFrameVariants`: s/a
- `EchoesHexConquestActiveStickers`: 三個任務的貼紙 uname
- `EchoesHexConquestHardModeStatus`: s/a
- `EchoesHexConquestUnlocked`: s/a
- `EchoesHexConquestCacheScoreMission`: s/a
- `EchoesHexConquestBonusTokensGiven`: 不知道，list[int] length 3

# KIM System
- `DialogueHistory`: 所有對話有關紀錄
- `RetroDisableKissInboxMessage`: kim 設定
- `RetroFastTyping`: s/a
- `RetroPlayAllConvos`: s/a
- `RetroWallpaperId`: s/a

# Unknown / Unimportant
(沒寫就是不知道 / 望文生義 / 雖然望文生義不出來但是就真的不太會用到所以連寫都不想寫)

- `ChallengesFixVersion`: 
- `TauntHistory`: 
- `TrainingDate`: 
- `SentientSpawnChanceBoosters`: 
- `ArchwingEnabled`: archwing 相關
- `Alignment`: 
- `CompletedSyndicates`: 
- `FactionScores`: 
- `PeriodicMissionCompletions`: 
- `HWIDProtectEnabled`: 
- `PendingTrades`: 
- `Settings`: 
- `CompletedSorties`: 
- `LastSortieReward`: 
- `CrewShipAmmo`
- `LotusCustomization`: 
- `UseAdultOperatorLoadout`: 用的是 operator 還是 drifter
- `RecentVendorPurchases`: 
- `PersonalGoalProgress`: 
- `CompletedAlerts`: 
- `EndlessXP`: circuit 獎勵
- `BountyScore`: 
- `LastLiteSortieReward`: archon hunt
- `SortieRewardAttenuation`: 
- `SongChallenges`: duviri 小遊戲
- `HubNpcCustomizations`: 
- `CompletedJobChains`: 
- `NemesisHistory`: Kuva / tenet / coda
- `EquippedEmotes`: 
- `Motorcycles`: 
- `CustomMarkers`: 開放地圖的 loc-pin
- `OperatorCustomizationSlotPurchases`: 
- `SpecialItemRewardAttenuation`: baro 的那個 cache 的 attenuation
- `CalendarProgress`: calendar
- `NokkoColony`: 蘑菇
- `DescentRewards`: descendia
- `FocusLoadouts`: focus 有關但不知道在幹嘛
- `LastNemesisAllySpawnTime`: 
- `QualifyingInvasions`: 
- `WeeklyGuildVaultBonusInfo`: 
- `NemesisAbandonedRewards`: 
- `Sketches`: follie
- `AlignmentReplay`: 
- `NewItems`: 
- `MiscAccountData`: 真的沒記甚麼，目前是記 tennocon 的某個變數
- `LastInventorySync`: 存的是 oid
- `NextRefill`: 具體上是甚麼不知道，猜每周或每日
- `ClaimedJunctionChallengeRewards`: junction
- `HasOwnedVoidProjectionsPreviously`: 完全不知道，我是 true
- `CollectibleSeries`: 老實說沒有很知道，我在猜是 entrati 那邊打書有的掃描和 kuria？
- `LibraryAvailableDailyTaskInfo`: 黃臉的每日
- `HasResetAccount`: false
- `PendingCoupon`: 
- `Harvestable`: 
- `NodeIntrosCompleted`: 我在猜是有沒有看過任意 cutscene，沒有很確定
- `DeathSquadable'`: 