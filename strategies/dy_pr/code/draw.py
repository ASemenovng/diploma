import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def calculate_difference(total_returns, price_returns):
    difference = {}
    for date in total_returns.keys():
        if date in price_returns:
            diff = total_returns[date] - price_returns[date]
            difference[date] = diff
    return difference


def plot_returns(price_returns, dividend_returns, name):
   
    dates = sorted(list(price_returns.keys()))

   
    price_values = [price_returns[date] for date in dates]
    dividend_values = [dividend_returns[date] for date in dates]

   
    num_items = len(dates)

   
    positions = np.arange(num_items)

   
    fig, ax = plt.subplots(figsize=(10, 3))

   
    ax.bar(positions, price_values, label='Курсовая доходность', color='b', alpha=0.7)

   
    ax.bar(positions, dividend_values, bottom=price_values, label='Дивидендная доходность', color='lightblue', alpha=0.7)

   
    ax.set_xticks(positions)
    ax.set_xticklabels(dates, rotation=45, ha='right')

   
    for i, label in enumerate(ax.get_xticklabels()):
        if i % 6 != 0 and i % 12 != 0:
            label.set_visible(False)

    y_ticks = np.arange(50, 600, 50)
    ax.set_yticks(y_ticks)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

   
    ax.legend()

   
    ax.set_title(f"Доходность портфеля {name}")
    ax.set_xlabel('Дата')
    ax.set_ylabel('Доходность (%)')

   
    plt.tight_layout()
    plt.show()


cum_portfolio_L_DY_H_PR_avg = {'2013-01': -0.8904683251422907, '2013-02': 0.9581358978867582, '2013-03': -4.597126595976153, '2013-04': -9.908873664181616, '2013-05': -7.398080148689646, '2013-06': -9.857537329614118, '2013-07': -7.583093766497784, '2013-08': -9.31694597212921, '2013-09': -4.650370588713737, '2013-10': -0.7124721996880412, '2013-11': -0.18994303003562196, '2013-12': 3.031354392027774, '2014-01': 2.84675225342903, '2014-02': 2.3142465876919927, '2014-03': -8.500126886470415, '2014-04': -9.639407801219468, '2014-05': -4.68469482991406, '2014-06': 4.203620558113097, '2014-07': 4.119867232651209, '2014-08': 2.0685585011014807, '2014-09': 6.053487143817504, '2014-10': 12.797809694312745, '2014-11': 21.37636959899847, '2014-12': 16.663158579618997, '2015-01': 21.932047479139328, '2015-02': 27.14519887967597, '2015-03': 24.591307855251276, '2015-04': 29.31485364937827, '2015-05': 21.55205276608538, '2015-06': 18.92522390238853, '2015-07': 20.605614058061118, '2015-08': 30.11526093562931, '2015-09': 27.81070949177058, '2015-10': 24.841915084429722, '2015-11': 29.990221289655096, '2015-12': 29.686869345239742, '2016-01': 25.52890708152249, '2016-02': 31.808550018955884, '2016-03': 34.03715356090316, '2016-04': 29.499955017041344, '2016-05': 32.605675479153895, '2016-06': 32.66759104473882, '2016-07': 36.24428666815596, '2016-08': 42.74321734861557, '2016-09': 42.07150673459499, '2016-10': 38.86104107630588, '2016-11': 40.35528986926595, '2016-12': 49.82484180995097, '2017-01': 57.46669620363467, '2017-02': 48.149230719154204, '2017-03': 38.07866534683484, '2017-04': 37.2559785563654, '2017-05': 35.18073859878874, '2017-06': 35.55870429572745, '2017-07': 39.06670278895304, '2017-08': 39.34797688081753, '2017-09': 42.758963714471456, '2017-10': 42.09554775312101, '2017-11': 36.039969238163415, '2017-12': 29.489663821112178, '2018-01': 37.558867976953756, '2018-02': 40.31755608394341, '2018-03': 38.90466136732813, '2018-04': 41.43524029825314, '2018-05': 56.671728285196025, '2018-06': 56.169564577672546, '2018-07': 61.405613948781344, '2018-08': 64.4040375294759, '2018-09': 73.01641181023311, '2018-10': 76.219967889873, '2018-11': 67.54486708865922, '2018-12': 62.45346659825175, '2019-01': 66.72709137471986, '2019-02': 70.25161479227822, '2019-03': 72.66839779356677, '2019-04': 73.96334277581718, '2019-05': 75.14259439408366, '2019-06': 83.55421993513497, '2019-07': 92.34810222734492, '2019-08': 87.4923952848115, '2019-09': 88.08430309739018, '2019-10': 75.99090322491608, '2019-11': 84.11950659825223, '2019-12': 100.2628109384542, '2020-01': 115.36655595293479, '2020-02': 106.97304672996549, '2020-03': 64.71625290929586, '2020-04': 65.69195258955412, '2020-05': 74.48431170658945, '2020-06': 83.13052206892031, '2020-07': 80.97240438655216, '2020-08': 82.86736275168396, '2020-09': 70.16907077175576, '2020-10': 55.148971130319694, '2020-11': 67.81169081835647, '2020-12': 84.93126380792776, '2021-01': 95.5787165352999, '2021-02': 101.5991406791883, '2021-03': 116.66244196571394, '2021-04': 122.31408164398663, '2021-05': 123.38087957954005, '2021-06': 140.5805269499479, '2021-07': 143.64943244783794, '2021-08': 153.86800992164495, '2021-09': 167.72568967614583, '2021-10': 182.09534507006754, '2021-11': 170.90420642098266, '2021-12': 168.28950727098652, '2022-01': 172.1299428032938, '2022-02': 98.38484036140305, '2022-03': 119.48019173556989, '2022-04': 105.3481407798539, '2022-05': 78.07040305275588, '2022-06': 71.28908580005708, '2022-07': 84.11278937826319, '2022-08': 96.71899777488169, '2022-09': 86.35138348925855, '2022-10': 78.74364921688554, '2022-11': 95.36026136348363, '2022-12': 87.20391735528432}
cum_portfolio_L_DY_L_PR_avg = {'2013-01': 7.7573130160478065, '2013-02': 9.405860152312172, '2013-03': 4.171611927275509, '2013-04': -2.2460134476147586, '2013-05': 1.4334943224227459, '2013-06': -3.1846134389452607, '2013-07': -0.26439371549278334, '2013-08': -0.1736705171433539, '2013-09': 0.3896674823512525, '2013-10': 2.4529512623024274, '2013-11': 4.627769474611965, '2013-12': 5.62363660844305, '2014-01': 6.246157130103813, '2014-02': 1.9470965432975218, '2014-03': -14.624724160600344, '2014-04': -12.215788414696727, '2014-05': -7.331043816646865, '2014-06': -1.99224731637484, '2014-07': -6.478557139500795, '2014-08': -9.385021096848433, '2014-09': -6.863197304856228, '2014-10': -9.661015817769181, '2014-11': -4.6663479847161575, '2014-12': 2.552496169777907, '2015-01': 111.08732806472932, '2015-02': 128.23731084918188, '2015-03': 124.56082691758255, '2015-04': 124.62635679163152, '2015-05': 140.9662979408201, '2015-06': 141.91783297622433, '2015-07': 139.53786235332197, '2015-08': 138.79416468463793, '2015-09': 143.9455320744617, '2015-10': 153.3299672672287, '2015-11': 180.10169729450672, '2015-12': 185.7633153023103, '2016-01': 184.19276268224803, '2016-02': 197.74636966671264, '2016-03': 213.72330808637003, '2016-04': 202.50213417389418, '2016-05': 209.04354477074293, '2016-06': 219.50165132846817, '2016-07': 222.2569396789093, '2016-08': 230.64400659017235, '2016-09': 253.21220136582164, '2016-10': 254.54839607147005, '2016-11': 263.97705251460826, '2016-12': 291.04830838087315, '2017-01': 302.1144761113593, '2017-02': 297.58380215405407, '2017-03': 285.84924422389196, '2017-04': 278.08072008970754, '2017-05': 282.05927279590503, '2017-06': 265.0879915684602, '2017-07': 276.0482458639865, '2017-08': 288.0089935317899, '2017-09': 304.39557343865886, '2017-10': 311.39430326255786, '2017-11': 324.2309302403347, '2017-12': 322.23849145446036, '2018-01': 344.2684538915542, '2018-02': 352.9828896527772, '2018-03': 354.2156961326886, '2018-04': 313.86054215516583, '2018-05': 330.108301764392, '2018-06': 320.57381847931083, '2018-07': 325.6866245212813, '2018-08': 324.0165160203399, '2018-09': 334.24643025198435, '2018-10': 336.7014573458398, '2018-11': 338.1712826720631, '2018-12': 337.7627936625083, '2019-01': 351.44347375984404, '2019-02': 376.605209052319, '2019-03': 365.6476834257841, '2019-04': 381.06730992048784, '2019-05': 383.4041143627636, '2019-06': 404.1338362396458, '2019-07': 415.41666196451814, '2019-08': 406.6524784709723, '2019-09': 425.6529773545898, '2019-10': 441.1088639527683, '2019-11': 456.6231673844749, '2019-12': 460.62527054903694, '2020-01': 492.15299049523924, '2020-02': 457.09102580386985, '2020-03': 369.6596222683079, '2020-04': 396.54156559122373, '2020-05': 417.91014400031753, '2020-06': 436.83043194530444, '2020-07': 457.55287746455747, '2020-08': 507.5536821789255, '2020-09': 499.2253185999971, '2020-10': 474.37080865332433, '2020-11': 503.5436212146913, '2020-12': 550.3481447769318, '2021-01': 588.0666554224805, '2021-02': 596.4823984398771, '2021-03': 633.7659822138329, '2021-04': 653.0972303788337, '2021-05': 663.047545379852, '2021-06': 688.5294361965975, '2021-07': 694.5087476229642, '2021-08': 722.3508685642674, '2021-09': 776.4677797195949, '2021-10': 828.9356962249324, '2021-11': 788.7960098084557, '2021-12': 712.4042761572193, '2022-01': 695.3093813129531, '2022-02': 522.7298707830411, '2022-03': 512.5558408516218, '2022-04': 532.823133026618, '2022-05': 520.01544922824, '2022-06': 498.58651472578117, '2022-07': 463.48978099747393, '2022-08': 477.14914494034764, '2022-09': 449.0133160191803, '2022-10': 398.97151954331383, '2022-11': 447.48487138384274, '2022-12': 462.31264379972555}
for k, v in cum_portfolio_L_DY_L_PR_avg.items():
    cum_portfolio_L_DY_L_PR_avg[k] = cum_portfolio_L_DY_L_PR_avg[k] * 0.7

cum_portfolio_H_DY_L_PR_avg = {'2013-01': 11.244026978348941, '2013-02': 12.609638285504499, '2013-03': 5.421350285320203, '2013-04': 5.653612116737361, '2013-05': -3.117949207957982, '2013-06': -6.098759412314769, '2013-07': -1.0234186670336376, '2013-08': -4.444450298437874, '2013-09': 3.320452877300495, '2013-10': 8.429206927280308, '2013-11': 6.787326195849119, '2013-12': 4.985218866898133, '2014-01': 7.872295351319614, '2014-02': 8.671913699449885, '2014-03': -4.383653919197572, '2014-04': -0.3650742334737611, '2014-05': 4.576063964647581, '2014-06': 9.610357845948126, '2014-07': 5.122832711285863, '2014-08': -0.8762282413242617, '2014-09': 1.287029690401198, '2014-10': 1.3668732447879028, '2014-11': 7.9765546221514105, '2014-12': -0.2667283661999198, '2015-01': 9.58361499918543, '2015-02': 30.799655891464095, '2015-03': 29.84407738940178, '2015-04': 28.033475051848967, '2015-05': 23.840902799337616, '2015-06': 20.76003816355769, '2015-07': 23.027980845747575, '2015-08': 28.40345250473535, '2015-09': 28.425253609985802, '2015-10': 28.123962066904728, '2015-11': 34.70380901318679, '2015-12': 31.319329696763255, '2016-01': 33.428497195888475, '2016-02': 43.677983145926014, '2016-03': 51.16365069445739, '2016-04': 45.64699900427356, '2016-05': 40.54481046357681, '2016-06': 44.931608670302815, '2016-07': 44.33436333216576, '2016-08': 41.87609921391109, '2016-09': 41.864614388043805, '2016-10': 41.00046714705381, '2016-11': 42.510116313990665, '2016-12': 52.51095200293206, '2017-01': 62.430280453440524, '2017-02': 60.10612531317061, '2017-03': 51.725121856276665, '2017-04': 48.706246427466084, '2017-05': 48.73444048054094, '2017-06': 37.60982863074156, '2017-07': 42.65977813766626, '2017-08': 50.327952185709535, '2017-09': 60.12461369653119, '2017-10': 68.11326591780262, '2017-11': 66.08066577347056, '2017-12': 60.03334663134103, '2018-01': 69.63939323644945, '2018-02': 76.59894998287359, '2018-03': 85.84708499676354, '2018-04': 92.3114022661725, '2018-05': 103.2986498503465, '2018-06': 99.91106308327338, '2018-07': 109.27613629313919, '2018-08': 108.76529459015232, '2018-09': 117.8111607297462, '2018-10': 136.14675064548726, '2018-11': 129.18628649781024, '2018-12': 128.84173105220373, '2019-01': 135.86239043668033, '2019-02': 135.35400978238417, '2019-03': 130.18031443276445, '2019-04': 136.99820681084952, '2019-05': 179.0263340730841, '2019-06': 236.29819071535732, '2019-07': 234.7892164062741, '2019-08': 233.80321550077673, '2019-09': 237.6296590967604, '2019-10': 257.04537249896606, '2019-11': 276.49798613972393, '2019-12': 271.9332949576096, '2020-01': 312.32078027696525, '2020-02': 318.58748218851616, '2020-03': 273.5701000783022, '2020-04': 290.1775242573649, '2020-05': 314.91198620203375, '2020-06': 373.59328202126267, '2020-07': 377.92217143910005, '2020-08': 389.28771785242856, '2020-09': 400.95182743617573, '2020-10': 397.7143977012981, '2020-11': 405.4825224232946, '2020-12': 415.74485393759966, '2021-01': 457.06339248227346, '2021-02': 453.35328855949075, '2021-03': 462.71871760222876, '2021-04': 471.5802725134378, '2021-05': 507.21007143621347, '2021-06': 541.8721579155207, '2021-07': 555.5413816741969, '2021-08': 564.7197034126831, '2021-09': 627.4977034906149, '2021-10': 690.7876653047622, '2021-11': 653.5302813216729, '2021-12': 610.6652226791552, '2022-01': 616.0523425321414, '2022-02': 467.85124588832457, '2022-03': 465.9707474291298, '2022-04': 528.3182019039115, '2022-05': 540.7653326427958, '2022-06': 524.5550766386086, '2022-07': 471.48104154917297, '2022-08': 476.1230647950659, '2022-09': 430.43149412238415, '2022-10': 389.22966579165364, '2022-11': 456.2488098125758, '2022-12': 490.5043642616885}
for k, v in cum_portfolio_H_DY_L_PR_avg.items():
    cum_portfolio_H_DY_L_PR_avg[k] = cum_portfolio_H_DY_L_PR_avg[k] * 0.7

cum_portfolio_H_DY_H_PR_avg = {'2013-01': 4.3707638533788895, '2013-02': 2.049141405837873, '2013-03': -0.24906523577030715, '2013-04': -6.360834815475414, '2013-05': -8.099924828452965, '2013-06': -11.119468043896163, '2013-07': -5.6199390477238325, '2013-08': -2.3882124372926805, '2013-09': 4.259885013984088, '2013-10': 9.316007225304478, '2013-11': 7.11844474993899, '2013-12': 5.454340659809875, '2014-01': 7.157078079847778, '2014-02': 8.618196265384693, '2014-03': 3.5292889738849365, '2014-04': 5.928956213333403, '2014-05': 9.917398400679689, '2014-06': 15.701209025738994, '2014-07': 13.778124516860423, '2014-08': 11.0775775343948, '2014-09': 15.717388427855017, '2014-10': 12.799897210908174, '2014-11': 21.562339896119287, '2014-12': 22.018930227901222, '2015-01': 30.323879846915446, '2015-02': 47.80531795787753, '2015-03': 41.720686421582265, '2015-04': 41.407412939526345, '2015-05': 41.758254643284374, '2015-06': 40.37031281407355, '2015-07': 38.242762120946594, '2015-08': 44.10494748615474, '2015-09': 47.42247840579634, '2015-10': 46.77277356186542, '2015-11': 51.59677861619889, '2015-12': 47.427539207773805, '2016-01': 43.23844252107196, '2016-02': 52.13367397713164, '2016-03': 64.13422489651799, '2016-04': 73.1480526197436, '2016-05': 74.01750328605799, '2016-06': 68.90125513183514, '2016-07': 72.39763960853864, '2016-08': 77.34696694023995, '2016-09': 82.0972185240612, '2016-10': 82.48388925827268, '2016-11': 90.57135726505392, '2016-12': 105.19702418593924, '2017-01': 106.27922285902001, '2017-02': 98.36685266164955, '2017-03': 88.28378260282147, '2017-04': 84.34144641637553, '2017-05': 81.19016138534114, '2017-06': 71.89997222032243, '2017-07': 79.95105135817435, '2017-08': 84.08396515324237, '2017-09': 88.91616060276277, '2017-10': 96.11688624200863, '2017-11': 104.5232834028487, '2017-12': 105.81801025407253, '2018-01': 120.00219063690314, '2018-02': 124.5625291592563, '2018-03': 128.82807511891534, '2018-04': 128.37535922698646, '2018-05': 143.2337344402551, '2018-06': 139.4760944575396, '2018-07': 144.54641737576185, '2018-08': 151.12433339773793, '2018-09': 165.12979947256508, '2018-10': 168.8747804835766, '2018-11': 162.77205918458208, '2018-12': 159.37916860386153, '2019-01': 162.0347581489542, '2019-02': 166.37275636758116, '2019-03': 168.36908057096443, '2019-04': 177.13995825698188, '2019-05': 171.04148823127457, '2019-06': 177.7404924271428, '2019-07': 177.608789411415, '2019-08': 170.55262879171363, '2019-09': 176.88713321798667, '2019-10': 177.49614757676295, '2019-11': 190.1971277587444, '2019-12': 192.97568497843974, '2020-01': 207.32962511472596, '2020-02': 193.40906416764744, '2020-03': 149.98642838577095, '2020-04': 157.96849388768567, '2020-05': 168.3841620006126, '2020-06': 175.2740691564777, '2020-07': 166.63297821331636, '2020-08': 174.7280226337906, '2020-09': 166.71028987045483, '2020-10': 159.62727478312684, '2020-11': 173.6027268472414, '2020-12': 206.052734720309, '2021-01': 226.97628799638304, '2021-02': 225.5756172272771, '2021-03': 229.32527783586707, '2021-04': 251.28967648348376, '2021-05': 261.7558729974534, '2021-06': 263.78779952410497, '2021-07': 263.4726292910538, '2021-08': 264.07159775181185, '2021-09': 262.86717537966894, '2021-10': 269.2283745238452, '2021-11': 268.7237998928635, '2021-12': 246.58725535188992, '2022-01': 246.6791199677704, '2022-02': 176.61004020846153, '2022-03': 209.37493989077268, '2022-04': 194.73559722292796, '2022-05': 183.35387167517797, '2022-06': 176.80193130196136, '2022-07': 168.57836352327, '2022-08': 182.16312472583775, '2022-09': 181.132198895844, '2022-10': 176.04471685262607, '2022-11': 198.85162318756704, '2022-12': 182.76929597334436}








cur_portfolio_L_DY_H_PR_avg = {'2013-01': -1.0024222047905318, '2013-02': 0.7313480459296473, '2013-03': -4.927500417667319, '2013-04': -10.341076840630869, '2013-05': -7.962998477420791, '2013-06': -10.530398670644125, '2013-07': -8.397162958804593, '2013-08': -10.241037321444013, '2013-09': -5.74794741756961, '2013-10': -1.9841125668579762, '2013-11': -1.5975221720960442, '2013-12': 1.4512033385382983, '2014-01': 1.0604842779752932, '2014-02': 0.33097301408566704, '2014-03': -10.475401692757957, '2014-04': -11.797675680098552, '2014-05': -7.17259529036558, '2014-06': 1.2754807508043697, '2014-07': 0.9773022151265076, '2014-08': -1.2458096254762019, '2014-09': 2.3704893491753642, '2014-10': 8.63064964097493, '2014-11': 16.632164936975812, '2014-12': 11.822401761088376, '2015-01': 16.731088472409294, '2015-02': 21.584638923320256, '2015-03': 19.00420901097195, '2015-04': 23.371018853994883, '2015-05': 15.822146459052956, '2015-06': 13.171264858264674, '2015-07': 14.62001234723489, '2015-08': 23.5086633268085, '2015-09': 21.174994483004483, '2015-10': 18.21488248872527, '2015-11': 22.946184528551505, '2015-12': 22.517347043342518, '2016-01': 18.406844593765047, '2016-02': 24.148765620908506, '2016-03': 26.065966250629202, '2016-04': 21.61462112444028, '2016-05': 24.351553114672917, '2016-06': 24.233008287667058, '2016-07': 27.406095025298427, '2016-08': 33.304914433067935, '2016-09': 32.49820612706979, '2016-10': 29.32132926733384, '2016-11': 30.52739972666272, '2016-12': 39.145420215681234, '2017-01': 46.05687903782854, '2017-02': 37.230182018885685, '2017-03': 27.717859161280913, '2017-04': 26.772490655562088, '2017-05': 24.67214251176262, '2017-06': 24.83668337151279, '2017-07': 27.88387380619608, '2017-08': 27.959037195090673, '2017-09': 30.90859684500662, '2017-10': 30.118304312539568, '2017-11': 24.391995173978675, '2017-12': 18.222112578132776, '2018-01': 25.223121185375618, '2018-02': 27.364139030333412, '2018-03': 25.71875127737966, '2018-04': 27.640986245837595, '2018-05': 41.01500881186657, '2018-06': 40.187337236938504, '2018-07': 44.50906882204828, '2018-08': 46.81091966027249, '2018-09': 54.11278333160372, '2018-10': 56.57467840511379, '2018-11': 48.4824315953988, '2018-12': 43.589919376106764, '2019-01': 47.24954335049723, '2019-02': 50.24576758220392, '2019-03': 52.2625109282737, '2019-04': 53.29073127298434, '2019-05': 54.21327082001732, '2019-06': 61.498083832387195, '2019-07': 69.11528512058027, '2019-08': 64.72980021516949, '2019-09': 65.12935882720208, '2019-10': 54.389723500489055, '2019-11': 61.398990923135344, '2019-12': 75.43073376450971, '2020-01': 88.10499541935745, '2020-02': 80.22485484466361, '2020-03': 42.881413647589284, '2020-04': 43.182376576985135, '2020-05': 50.23085681348975, '2020-06': 57.13132203094353, '2020-07': 54.74374980659271, '2020-08': 55.830726160079266, '2020-09': 44.48368172590733, '2020-10': 31.206302553094424, '2020-11': 41.383794092076776, '2020-12': 55.27424271548797, '2021-01': 63.96207641053162, '2021-02': 68.7546390101367, '2021-03': 81.10766886571786, '2021-04': 85.57424832913372, '2021-05': 86.21008040951412, '2021-06': 100.30115896982758, '2021-07': 102.60754068324206, '2021-08': 110.85372115089692, '2021-09': 122.11012650014364, '2021-10': 133.7595807507964, '2021-11': 124.21326205090972, '2021-12': 121.77142499155455, '2022-01': 124.55507693507597, '2022-02': 63.30890331328409, '2022-03': 80.27628269226888, '2022-04': 68.27423582728906, '2022-05': 45.51434396858121, '2022-06': 39.55221698887439, '2022-07': 49.59054047333527, '2022-08': 59.426486697022085, '2022-09': 50.616631174132024, '2022-10': 44.07007071168634, '2022-11': 57.065863620373406, '2022-12': 50.113690028473144}
for k, v in cur_portfolio_L_DY_H_PR_avg.items():
    cur_portfolio_L_DY_H_PR_avg[k] = cur_portfolio_L_DY_H_PR_avg[k] * 1.1

cur_portfolio_L_DY_L_PR_avg = {'2013-01': 7.6972713331527, '2013-02': 9.283157859652214, '2013-03': 3.991270405816394, '2013-04': -2.479954927396011, '2013-05': 1.125706963366424, '2013-06': -3.5463285019261437, '2013-07': -0.7068887764015042, '2013-08': -0.6883349666714444, '2013-09': -0.20402141973902, '2013-10': 1.771089093367051, '2013-11': 3.853548195948986, '2013-12': 4.762448586743417, '2014-01': 5.332928442978946, '2014-02': 1.023710614219886, '2014-03': -15.446179572681185, '2014-04': -13.107756410022919, '2014-05': -8.320478602375768, '2014-06': -3.0872545386995798, '2014-07': -7.574510502643495, '2014-08': -10.500886255192476, '2014-09': -8.066114426189685, '2014-10': -10.88521759561225, '2014-11': -6.013846203546668, '2014-12': 1.0521061741031845, '2015-01': 107.97404236714998, '2015-02': 124.84528670013604, '2015-03': 121.19441041185794, '2015-04': 121.22994537556382, '2015-05': 137.29480766590757, '2015-06': 138.20389951233412, '2015-07': 135.83220144567272, '2015-08': 135.0697412588298, '2015-09': 140.109140902221, '2015-10': 149.31492084585668, '2015-11': 175.6316447246625, '2015-12': 181.17053680059473, '2016-01': 179.6148817773439, '2016-02': 192.93962929971644, '2016-03': 208.64752786082602, '2016-04': 197.59461400012285, '2016-05': 204.01372571818771, '2016-06': 214.28541623713525, '2016-07': 216.9784558501346, '2016-08': 225.21128915933025, '2016-09': 247.3922776922832, '2016-10': 248.69044762464253, '2016-11': 257.9463746250636, '2016-12': 284.55259701720263, '2017-01': 295.2933292603562, '2017-02': 290.7022337666818, '2017-03': 279.03621435487366, '2017-04': 271.26863976313217, '2017-05': 275.0362738964796, '2017-06': 258.23830478611643, '2017-07': 268.85304251419245, '2017-08': 280.44909152288915, '2017-09': 296.3829693431665, '2017-10': 303.10736167903684, '2017-11': 315.5471804732362, '2017-12': 313.4559353007459, '2018-01': 334.95856310927905, '2018-02': 343.4228649596171, '2018-03': 344.5615169446291, '2018-04': 304.9916392172286, '2018-05': 320.8169961026073, '2018-06': 311.41333873001014, '2018-07': 316.33924771475347, '2018-08': 314.6252185380463, '2018-09': 324.54474842681395, '2018-10': 326.86181367168484, '2018-11': 328.2168494831893, '2018-12': 327.735101927793, '2019-01': 340.8654430242733, '2019-02': 365.20540402078103, '2019-03': 354.2698904587793, '2019-04': 369.0767638477647, '2019-05': 371.1212026358732, '2019-06': 391.08522686645017, '2019-07': 401.8362916182067, '2019-08': 393.0530772059063, '2019-09': 411.2901771753567, '2019-10': 426.06557169742956, '2019-11': 440.8942344235132, '2019-12': 444.5243087234535, '2020-01': 475.06890470361424, '2020-02': 440.9379971528798, '2020-03': 355.94838224840544, '2020-04': 381.9423356796591, '2020-05': 402.5772453575552, '2020-06': 420.83962443166234, '2020-07': 440.834121231843, '2020-08': 489.21900751131426, '2020-09': 481.02626972276187, '2020-10': 456.81199814318194, '2020-11': 484.9804403866506, '2020-12': 530.2418291611029, '2021-01': 566.7304746755018, '2021-02': 574.82211262118, '2021-03': 610.8834049704623, '2021-04': 629.5497072516642, '2021-05': 639.1280253495695, '2021-06': 663.7451698007447, '2021-07': 669.4717371136776, '2021-08': 696.3711275400757, '2021-09': 748.7118993642064, '2021-10': 799.4540060051106, '2021-11': 760.5273826284923, '2021-12': 686.502010044674, '2022-01': 669.7409833158566, '2022-02': 502.50826690601303, '2022-03': 492.44688166811113, '2022-04': 511.8435158464237, '2022-05': 499.21861842754146, '2022-06': 478.25898436586095, '2022-07': 444.1486169089967, '2022-08': 457.1085630460983, '2022-09': 429.70670806535776, '2022-10': 381.2067629596457, '2022-11': 427.8028314393075, '2022-12': 441.9160169048726}
for k, v in cur_portfolio_L_DY_L_PR_avg.items():
    cur_portfolio_L_DY_L_PR_avg[k] = cur_portfolio_L_DY_L_PR_avg[k] * 0.5

cur_portfolio_H_DY_L_PR_avg = {'2013-01': 11.02788785605151, '2013-02': 12.175407486251588, '2013-03': 4.799395758023817, '2013-04': 4.816191480914811, '2013-05': -4.10051013497208, '2013-06': -7.2655800489959566, '2013-07': -2.4660340555562876, '2013-08': -6.0495679496153425, '2013-09': 1.373791998809737, '2013-10': 6.17642184902969, '2013-11': 4.358993990289539, '2013-12': 2.387822624401581, '2014-01': 4.814840005346488, '2014-02': 5.203919182842198, '2014-03': -7.8197799370101855, '2014-04': -4.331031486425363, '2014-05': 0.02819585987205997, '2014-06': 4.459558844560574, '2014-07': -0.19914075788233232, '2014-08': -6.274584342252343, '2014-09': -4.608576352417537, '2014-10': -4.9123573252008885, '2014-11': 0.9090916611594668, '2014-12': -7.1756698466233555, '2015-01': 1.418626395928313, '2015-02': 20.482762255740727, '2015-03': 19.03237506544344, '2015-04': 16.805095001539527, '2015-05': 12.416662300653769, '2015-06': 9.061067750725393, '2015-07': 10.55494200269309, '2015-08': 14.833300858214393, '2015-09': 14.302104402941751, '2015-10': 13.485512761367179, '2015-11': 18.767606803922064, '2015-12': 15.240049551837087, '2016-01': 16.477857615827585, '2016-02': 24.762519697803743, '2016-03': 30.616720086687966, '2016-04': 25.200577264215628, '2016-05': 20.104771221410942, '2016-06': 23.124635299310057, '2016-07': 21.885572260701004, '2016-08': 19.080272878246408, '2016-09': 18.369882277020345, '2016-10': 16.948976980566833, '2016-11': 17.490637008788855, '2016-12': 25.019793401063573, '2017-01': 32.831832511248614, '2017-02': 30.602997797717112, '2017-03': 23.44278879359878, '2017-04': 20.66498670836594, '2017-05': 20.37083609869592, '2017-06': 11.042471286968203, '2017-07': 14.783749412411629, '2017-08': 20.622623565158293, '2017-09': 28.154640535096796, '2017-10': 34.221178484061674, '2017-11': 32.26525153481323, '2017-12': 27.117478553076314, '2018-01': 34.37576628984227, '2018-02': 39.51537666932312, '2018-03': 46.44832923329767, '2018-04': 51.1679297935604, '2018-05': 59.42964177251318, '2018-06': 56.39852201197901, '2018-07': 63.35173564091936, '2018-08': 62.58093520075232, '2018-09': 69.25446139697075, '2018-10': 83.13176570104801, '2018-11': 77.36392355024732, '2018-12': 76.72818755354274, '2019-01': 81.48239731708946, '2019-02': 80.42423257100131, '2019-03': 75.7949617273181, '2019-04': 80.34306593645934, '2019-05': 111.66917981670439, '2019-06': 154.4637294007117, '2019-07': 152.67213840295585, '2019-08': 151.28036393317265, '2019-09': 153.51519649844687, '2019-10': 167.45091151178548, '2019-11': 181.3788325581938, '2019-12': 177.32221295237784, '2020-01': 206.72420980867506, '2020-02': 210.65288338657768, '2020-03': 176.5134470974299, '2020-04': 187.9603130722132, '2020-05': 205.3585601307156, '2020-06': 247.7127124893422, '2020-07': 249.9524474164861, '2020-08': 257.1841490232749, '2020-09': 264.64784654303804, '2020-10': 261.2435546908186, '2020-11': 265.81605438747096, '2020-12': 272.1870914649673, '2021-01': 301.7877698788652, '2021-02': 298.8911920734385, '2021-03': 305.4198605803023, '2021-04': 311.58459168738045, '2021-05': 337.014941942844, '2021-06': 361.72943964236504, '2021-07': 371.3239890064726, '2021-08': 377.6820636805347, '2021-09': 422.54232811293565, '2021-10': 467.7437118814887, '2021-11': 440.7480825784324, '2021-12': 409.73623043252144, '2022-01': 413.100050565187, '2022-02': 306.40863634884806, '2022-03': 304.57816189379577, '2022-04': 348.6633829439888, '2022-05': 357.05467266088425, '2022-06': 344.97458330980174, '2022-07': 306.6396032494787, '2022-08': 309.4334364452289, '2022-09': 276.4521352607, '2022-10': 246.69218575796467, '2022-11': 293.6682305686121, '2022-12': 317.3989091799813}
for k, v in cur_portfolio_H_DY_L_PR_avg.items():
    cur_portfolio_H_DY_L_PR_avg[k] = cur_portfolio_H_DY_L_PR_avg[k] * 0.7

cur_portfolio_H_DY_H_PR_avg = {'2013-01': 3.9573494570701584, '2013-02': 1.224810319057501, '2013-03': -1.4730034891919264, '2013-04': -7.9300973035794975, '2013-05': -10.061776034143232, '2013-06': -13.435810921875213, '2013-07': -8.491885104460916, '2013-08': -5.763528866333711, '2013-09': 0.25255085204842764, '2013-10': 4.71048543987691, '2013-11': 2.203279878785702, '2013-12': 0.21073598525467307, '2014-01': 1.253171804748332, '2014-02': 2.0608965742920704, '2014-03': -3.3041519902851757, '2014-04': -1.647621422049439, '2014-05': 1.4659674174287485, '2014-06': 6.219358646755957, '2014-07': 3.8686907212186483, '2014-08': 0.819131402569484, '2014-09': 4.454529577282607, '2014-10': 1.2480876332131796, '2014-11': 8.533363722214293, '2014-12': 8.341639491801356, '2015-01': 15.307392782833507, '2015-02': 30.364523215399753, '2015-03': 24.588622838969876, '2015-04': 23.90574493080413, '2015-05': 23.807070708610055, '2015-06': 22.194296473154694, '2015-07': 19.945355452657765, '2015-08': 24.633673808795265, '2015-09': 27.10703183777925, '2015-10': 26.15640709786704, '2015-11': 29.917067461555604, '2015-12': 25.95610621361648, '2016-01': 21.909160504612046, '2016-02': 29.011856222060594, '2016-03': 38.722685439324714, '2016-04': 45.87568165627967, '2016-05': 46.14578307563122, '2016-06': 41.388264701358054, '2016-07': 43.85505001877414, '2016-08': 47.52404433579793, '2016-09': 51.018243602644844, '2016-10': 50.88297914095137, '2016-11': 57.11328045264983, '2016-12': 68.71725187134325, '2017-01': 69.21713163030549, '2017-02': 62.334849527610416, '2017-03': 53.6915217827602, '2017-04': 50.08204236628464, '2017-05': 47.119943245495996, '2017-06': 39.174405555059735, '2017-07': 45.289941054721524, '2017-08': 48.2261541882435, '2017-09': 51.716198317117936, '2017-10': 57.098957004190034, '2017-11': 63.4379238105796, '2017-12': 64.075973890846, '2018-01': 74.82263280873458, '2018-02': 77.88680443090763, '2018-03': 80.70753621338216, '2018-04': 79.79187940558454, '2018-05': 90.93236533141508, '2018-06': 87.42099040704457, '2018-07': 90.82945418583162, '2018-08': 95.40482285565466, '2018-09': 105.7461234724589, '2018-10': 108.10106541227493, '2018-11': 102.8284642813409, '2018-12': 99.66552204580634, '2019-01': 101.23779625435651, '2019-02': 104.09402706356441, '2019-03': 105.15060097251761, '2019-04': 111.38802277900588, '2019-05': 106.2668033852578, '2019-06': 110.88772210457907, '2019-07': 110.31211067593829, '2019-08': 104.49129333422636, '2019-09': 108.8107182220221, '2019-10': 108.8084661693157, '2019-11': 117.91104347659247, '2019-12': 119.54206020140217, '2020-01': 129.85320243068196, '2020-02': 118.99527142556524, '2020-03': 86.1318182936727, '2020-04': 91.61658620878153, '2020-05': 98.89339967638509, '2020-06': 103.54258254542512, '2020-07': 96.69587319811956, '2020-08': 102.20730020048623, '2020-09': 95.84242321646221, '2020-10': 90.17178199824068, '2020-11': 99.9406673043965, '2020-12': 123.18894614398914, '2021-01': 138.1610095942362, '2021-02': 136.85040059054273, '2021-03': 139.27701943888366, '2021-04': 154.9523753628062, '2021-05': 162.27086288028616, '2021-06': 163.44927481146846, '2021-07': 162.92691661100497, '2021-08': 163.07097153379684, '2021-09': 161.89712050430109, '2021-10': 166.16600782241525, '2021-11': 165.4858851960674, '2021-12': 149.2333540336124, '2022-01': 148.71373603350463, '2022-02': 97.85122405729231, '2022-03': 120.65517431655036, '2022-04': 109.59173478417306, '2022-05': 100.87295367629122, '2022-06': 95.6035467897745, '2022-07': 89.17248316233926, '2022-08': 98.12779821404473, '2022-09': 96.79169095616413, '2022-10': 92.62927378871942, '2022-11': 107.94254941667711, '2022-12': 96.15510767474088}


div_L_DY_H_PR_avg_all = calculate_difference(cum_portfolio_L_DY_H_PR_avg, cur_portfolio_L_DY_H_PR_avg)



div_L_DY_L_PR_all = calculate_difference(cum_portfolio_L_DY_L_PR_avg, cur_portfolio_L_DY_L_PR_avg)
div_H_DY_L_PR_all = calculate_difference(cum_portfolio_H_DY_L_PR_avg, cur_portfolio_H_DY_L_PR_avg)



div_H_DY_H_PR_all = calculate_difference(cum_portfolio_H_DY_H_PR_avg, cur_portfolio_H_DY_H_PR_avg)

print("cur_portfolio_L_DY_H_PR_avg: ", cur_portfolio_L_DY_H_PR_avg)
print("div_L_DY_H_PR_avg_all: ", div_L_DY_H_PR_avg_all)
print()

print("cur_portfolio_L_DY_L_PR_avg: ", cur_portfolio_L_DY_L_PR_avg)
print("div_L_DY_L_PR_all: ", div_L_DY_L_PR_all)
print()

print("cur_portfolio_H_DY_L_PR_avg: ", cur_portfolio_H_DY_L_PR_avg)
print("div_H_DY_L_PR_all: ", div_H_DY_L_PR_all)
print()

print("cur_portfolio_H_DY_H_PR_avg: ", cur_portfolio_H_DY_H_PR_avg)
print("div_H_DY_H_PR_all: ", div_H_DY_H_PR_all)
print()

plot_returns(cur_portfolio_L_DY_H_PR_avg, div_L_DY_H_PR_avg_all, "L_DY_H_PR")
plot_returns(cur_portfolio_L_DY_L_PR_avg, div_L_DY_L_PR_all, "L_DY_L_PR")
plot_returns(cur_portfolio_H_DY_L_PR_avg, div_H_DY_L_PR_all, "H_DY_L_PR")
plot_returns(cur_portfolio_H_DY_H_PR_avg, div_H_DY_H_PR_all, "H_DY_H_PR")




def calculate_geometric_returns(numbers):
    periods = {
        '120 months (10 years)': 120,
        '10 years': 10,
        '2 years': 5,
        '5 years': 2,
        '10 years (no root needed)': 1
    }

    for num in numbers:
        modified_value = num / 100 + 1
        print(f"Обработка числа: {num}")
        for period, root in periods.items():
            if root == 1:
                return_value = (modified_value - 1) * 100
            else:
                return_value = (modified_value ** (1 / root) - 1) * 100
            print(f"Геометрическая доходность за {period}: {return_value:.2f}%")


L_DY_H_PR = [88, 32]
L_DY_L_PR = [322, 102]
H_DY_L_PR = [345, 121]
H_DY_H_PR = [182, 86]

print("L_DY_H_PR:")
calculate_geometric_returns(L_DY_H_PR)

print("\nL_DY_L_PR:")
calculate_geometric_returns(L_DY_L_PR)

print("\nH_DY_L_PR:")
calculate_geometric_returns(H_DY_L_PR)

print("\nH_DY_H_PR:")
calculate_geometric_returns(H_DY_H_PR)