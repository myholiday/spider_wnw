#!/usr/bin/env python# -*- coding: utf-8 -*-# Created by spider3 on 2018/3/9# Copyright (c) 2018 spider3. All rights reserved."""高德地图poi: http://lbs.amap.com/api/webservice/guide/api/search/"""import jsonimport requestsimport timefrom pymongo import MongoClientfrom retry import retryfrom requests.exceptions import ConnectionErrorfrom utils.logger import init_loggerfrom queue import Queuefrom threading import Thread# 所有地区idaddr_ids = [110000, 110100, 110101, 110102, 110105, 110106, 110107, 110108, 110109, 110111, 110112, 110113, 110114,            110115, 110116, 110117, 110118, 110119, 120000, 120100, 120101, 120102, 120103, 120104, 120105, 120106,            120110, 120111, 120112, 120113, 120114, 120115, 120116, 120117, 120118, 120119, 130100, 130101, 130102,            130104, 130105, 130107, 130108, 130109, 130110, 130111, 130121, 130123, 130125, 130126, 130127, 130128,            130129, 130130, 130131, 130132, 130133, 130181, 130183, 130184, 130200, 130201, 130202, 130203, 130204,            130205, 130207, 130208, 130209, 130223, 130224, 130225, 130227, 130229, 130281, 130283, 130300, 130301,            130302, 130303, 130304, 130321, 130322, 130306, 130324, 130400, 130401, 130402, 130403, 130404, 130406,            130423, 130424, 130425, 130426, 130427, 130407, 130408, 130430, 130431, 130432, 130433, 130434, 130435,            130481, 130500, 130501, 130502, 130503, 130521, 130522, 130523, 130524, 130525, 130526, 130527, 130528,            130529, 130530, 130531, 130532, 130533, 130534, 130535, 130581, 130582, 130600, 130601, 130602, 130606,            130607, 130608, 130623, 130624, 130609, 130626, 130627, 130628, 130629, 130630, 130631, 130632, 130633,            130634, 130635, 130636, 130637, 130638, 130681, 130682, 130683, 130684, 130700, 130701, 130702, 130703,            130705, 130706, 130722, 130723, 130724, 130725, 130726, 130727, 130728, 130708, 130730, 130731, 130732,            130709, 130800, 130801, 130802, 130803, 130804, 130821, 130822, 130881, 130824, 130825, 130826, 130827,            130828, 130900, 130901, 130902, 130903, 130921, 130922, 130923, 130924, 130925, 130926, 130927, 130928,            130929, 130930, 130981, 130982, 130983, 130984, 131000, 131001, 131002, 131003, 131022, 131023, 131024,            131025, 131026, 131028, 131081, 131082, 131100, 131101, 131102, 131121, 131122, 131123, 131124, 131125,            131126, 131127, 131128, 131103, 131182, 140100, 140101, 140105, 140106, 140107, 140108, 140109, 140110,            140121, 140122, 140123, 140181, 140200, 140201, 140202, 140203, 140211, 140212, 140221, 140222, 140223,            140224, 140225, 140226, 140227, 140300, 140301, 140302, 140303, 140311, 140321, 140322, 140400, 140401,            140402, 140411, 140421, 140423, 140424, 140425, 140426, 140427, 140428, 140429, 140430, 140431, 140481,            140500, 140501, 140502, 140521, 140522, 140524, 140525, 140581, 140600, 140601, 140602, 140603, 140621,            140622, 140623, 140624, 140700, 140701, 140702, 140721, 140722, 140723, 140724, 140725, 140726, 140727,            140728, 140729, 140781, 140800, 140801, 140802, 140821, 140822, 140823, 140824, 140825, 140826, 140827,            140828, 140829, 140830, 140881, 140882, 140900, 140901, 140902, 140921, 140922, 140923, 140924, 140925,            140926, 140927, 140928, 140929, 140930, 140931, 140932, 140981, 141000, 141001, 141002, 141021, 141022,            141023, 141024, 141025, 141026, 141027, 141028, 141029, 141030, 141031, 141032, 141033, 141034, 141081,            141082, 141100, 141101, 141102, 141121, 141122, 141123, 141124, 141125, 141126, 141127, 141128, 141129,            141130, 141181, 141182, 150100, 150101, 150102, 150103, 150104, 150105, 150121, 150122, 150123, 150124,            150125, 150200, 150201, 150202, 150203, 150204, 150205, 150206, 150207, 150221, 150222, 150223, 150300,            150301, 150302, 150303, 150304, 150400, 150401, 150402, 150403, 150404, 150421, 150422, 150423, 150424,            150425, 150426, 150428, 150429, 150430, 150500, 150501, 150502, 150521, 150522, 150523, 150524, 150525,            150526, 150581, 150600, 150601, 150602, 150603, 150621, 150622, 150623, 150624, 150625, 150626, 150627,            150700, 150701, 150702, 150703, 150721, 150722, 150723, 150724, 150725, 150726, 150727, 150781, 150782,            150783, 150784, 150785, 150800, 150801, 150802, 150821, 150822, 150823, 150824, 150825, 150826, 150900,            150901, 150902, 150921, 150922, 150923, 150924, 150925, 150926, 150927, 150928, 150929, 150981, 152200,            152201, 152202, 152221, 152222, 152223, 152224, 152500, 152501, 152502, 152522, 152523, 152524, 152525,            152526, 152527, 152528, 152529, 152530, 152531, 152900, 152921, 152922, 152923, 210100, 210101, 210102,            210103, 210104, 210105, 210106, 210111, 210112, 210113, 210114, 210115, 210123, 210124, 210181, 210200,            210201, 210202, 210203, 210204, 210211, 210212, 210213, 210224, 210281, 210214, 210283, 210300, 210301,            210302, 210303, 210304, 210311, 210321, 210323, 210381, 210400, 210401, 210402, 210403, 210404, 210411,            210421, 210422, 210423, 210500, 210501, 210502, 210503, 210504, 210505, 210521, 210522, 210600, 210601,            210602, 210603, 210604, 210624, 210681, 210682, 210700, 210701, 210702, 210703, 210711, 210726, 210727,            210781, 210782, 210800, 210801, 210802, 210803, 210804, 210811, 210881, 210882, 210900, 210901, 210902,            210903, 210904, 210905, 210911, 210921, 210922, 211000, 211001, 211002, 211003, 211004, 211005, 211011,            211021, 211081, 211100, 211101, 211102, 211103, 211104, 211122, 211200, 211201, 211202, 211204, 211221,            211223, 211224, 211281, 211282, 211300, 211301, 211302, 211303, 211321, 211322, 211324, 211381, 211382,            211400, 211401, 211402, 211403, 211404, 211421, 211422, 211481, 220100, 220101, 220102, 220103, 220104,            220105, 220106, 220112, 220113, 220122, 220182, 220183, 220200, 220201, 220202, 220203, 220204, 220211,            220221, 220281, 220282, 220283, 220284, 220300, 220301, 220302, 220303, 220322, 220323, 220381, 220382,            220400, 220401, 220402, 220403, 220421, 220422, 220500, 220501, 220502, 220503, 220521, 220523, 220524,            220581, 220582, 220600, 220601, 220602, 220605, 220621, 220622, 220623, 220681, 220700, 220701, 220702,            220721, 220722, 220723, 220781, 220800, 220801, 220802, 220821, 220822, 220881, 220882, 222400, 222401,            222402, 222403, 222404, 222405, 222406, 222424, 222426, 230100, 230101, 230102, 230103, 230104, 230108,            230109, 230110, 230111, 230112, 230113, 230123, 230124, 230125, 230126, 230127, 230128, 230129, 230183,            230184, 230200, 230201, 230202, 230203, 230204, 230205, 230206, 230207, 230208, 230221, 230223, 230224,            230225, 230227, 230229, 230230, 230231, 230281, 230300, 230301, 230302, 230303, 230304, 230305, 230306,            230307, 230321, 230381, 230382, 230400, 230401, 230402, 230403, 230404, 230405, 230406, 230407, 230421,            230422, 230500, 230501, 230502, 230503, 230505, 230506, 230521, 230522, 230523, 230524, 230600, 230601,            230602, 230603, 230604, 230605, 230606, 230621, 230622, 230623, 230624, 230700, 230701, 230702, 230703,            230704, 230705, 230706, 230707, 230708, 230709, 230710, 230711, 230712, 230713, 230714, 230715, 230716,            230722, 230781, 230800, 230801, 230803, 230804, 230805, 230811, 230822, 230826, 230828, 230883, 230881,            230882, 230900, 230901, 230902, 230903, 230904, 230921, 231000, 231001, 231002, 231003, 231004, 231005,            231086, 231025, 231081, 231083, 231084, 231085, 231100, 231101, 231102, 231121, 231123, 231124, 231181,            231182, 231200, 231201, 231202, 231221, 231222, 231223, 231224, 231225, 231226, 231281, 231282, 231283,            232700, 232701, 232721, 232722, 232723, 310000, 310100, 310101, 310104, 310105, 310106, 310107, 310109,            310110, 310112, 310113, 310114, 310115, 310116, 310117, 310118, 310120, 310151, 320100, 320101, 320102,            320104, 320105, 320106, 320111, 320113, 320114, 320115, 320116, 320117, 320118, 320200, 320201, 320213,            320214, 320205, 320206, 320211, 320281, 320282, 320300, 320301, 320302, 320303, 320305, 320311, 320312,            320321, 320322, 320324, 320381, 320382, 320400, 320401, 320402, 320404, 320411, 320412, 320481, 320413,            320500, 320501, 320505, 320506, 320507, 320508, 320509, 320581, 320582, 320583, 320585, 320600, 320601,            320602, 320611, 320612, 320621, 320623, 320681, 320682, 320684, 320700, 320701, 320703, 320706, 320707,            320722, 320723, 320724, 320800, 320801, 320812, 320803, 320804, 320826, 320813, 320830, 320831, 320900,            320901, 320902, 320903, 320921, 320922, 320923, 320924, 320925, 320981, 320904, 321000, 321001, 321002,            321003, 321012, 321023, 321081, 321084, 321100, 321101, 321102, 321111, 321112, 321181, 321182, 321183,            321200, 321201, 321202, 321203, 321204, 321281, 321282, 321283, 321300, 321301, 321302, 321311, 321322,            321323, 321324, 330100, 330101, 330102, 330103, 330104, 330105, 330106, 330108, 330109, 330110, 330111,            330122, 330127, 330182, 330185, 330200, 330201, 330203, 330205, 330206, 330211, 330212, 330225, 330226,            330281, 330282, 330213, 330300, 330301, 330302, 330303, 330304, 330305, 330324, 330326, 330327, 330328,            330329, 330381, 330382, 330400, 330401, 330402, 330411, 330421, 330424, 330481, 330482, 330483, 330500,            330501, 330502, 330503, 330521, 330522, 330523, 330600, 330601, 330602, 330603, 330604, 330624, 330681,            330683, 330700, 330701, 330702, 330703, 330723, 330726, 330727, 330781, 330782, 330783, 330784, 330800,            330801, 330802, 330803, 330822, 330824, 330825, 330881, 330900, 330901, 330902, 330903, 330921, 330922,            331000, 331001, 331002, 331003, 331004, 331021, 331022, 331023, 331024, 331081, 331082, 331100, 331101,            331102, 331121, 331122, 331123, 331124, 331125, 331126, 331127, 331181, 340100, 340101, 340102, 340103,            340104, 340111, 340121, 340122, 340123, 340124, 340181, 340200, 340201, 340202, 340203, 340207, 340208,            340221, 340222, 340223, 340225, 340300, 340301, 340302, 340303, 340304, 340311, 340321, 340322, 340323,            340400, 340401, 340402, 340403, 340404, 340405, 340406, 340421, 340422, 340500, 340501, 340503, 340504,            340506, 340521, 340522, 340523, 340600, 340601, 340602, 340603, 340604, 340621, 340700, 340701, 340705,            340711, 340706, 340722, 340800, 340801, 340802, 340803, 340811, 340822, 340824, 340825, 340826, 340827,            340828, 340881, 341000, 341001, 341002, 341003, 341004, 341021, 341022, 341023, 341024, 341100, 341101,            341102, 341103, 341122, 341124, 341125, 341126, 341181, 341182, 341200, 341201, 341202, 341203, 341204,            341221, 341222, 341225, 341226, 341282, 341300, 341301, 341302, 341321, 341322, 341323, 341324, 341500,            341501, 341502, 341503, 341504, 341522, 341523, 341524, 341525, 341600, 341601, 341602, 341621, 341622,            341623, 341700, 341701, 341702, 341721, 341722, 341723, 341800, 341801, 341802, 341821, 341822, 341823,            341824, 341825, 341881, 350100, 350101, 350102, 350103, 350104, 350105, 350111, 350121, 350122, 350123,            350124, 350125, 350128, 350181, 350182, 350200, 350201, 350203, 350205, 350206, 350211, 350212, 350213,            350300, 350301, 350302, 350303, 350304, 350305, 350322, 350400, 350401, 350402, 350403, 350421, 350423,            350424, 350425, 350426, 350427, 350428, 350429, 350430, 350481, 350500, 350501, 350502, 350503, 350504,            350505, 350521, 350524, 350525, 350526, 350527, 350581, 350582, 350583, 350600, 350601, 350602, 350603,            350622, 350623, 350624, 350625, 350626, 350627, 350628, 350629, 350681, 350700, 350701, 350702, 350703,            350721, 350722, 350723, 350724, 350725, 350781, 350782, 350783, 350800, 350801, 350802, 350803, 350821,            350823, 350824, 350825, 350881, 350900, 350901, 350902, 350921, 350922, 350923, 350924, 350925, 350926,            350981, 350982, 360100, 360101, 360102, 360103, 360104, 360105, 360111, 360121, 360112, 360123, 360124,            360200, 360201, 360202, 360203, 360222, 360281, 360300, 360301, 360302, 360313, 360321, 360322, 360323,            360400, 360401, 360402, 360403, 360421, 360423, 360424, 360425, 360426, 360483, 360428, 360429, 360430,            360481, 360482, 360500, 360501, 360502, 360521, 360600, 360601, 360602, 360622, 360681, 360700, 360701,            360702, 360703, 360704, 360722, 360723, 360724, 360725, 360726, 360727, 360728, 360729, 360730, 360731,            360732, 360733, 360734, 360735, 360781, 360800, 360801, 360802, 360803, 360821, 360822, 360823, 360824,            360825, 360826, 360827, 360828, 360829, 360830, 360881, 360900, 360901, 360902, 360921, 360922, 360923,            360924, 360925, 360926, 360981, 360982, 360983, 361000, 361001, 361002, 361021, 361022, 361023, 361024,            361025, 361026, 361027, 361028, 361003, 361030, 361100, 361101, 361102, 361103, 361121, 361123, 361124,            361125, 361126, 361127, 361128, 361129, 361130, 361181, 370100, 370101, 370102, 370103, 370104, 370105,            370112, 370113, 370124, 370125, 370126, 370114, 370200, 370201, 370202, 370203, 370211, 370212, 370213,            370214, 370281, 370282, 370283, 370285, 370300, 370301, 370302, 370303, 370304, 370305, 370306, 370321,            370322, 370323, 370400, 370401, 370402, 370403, 370404, 370405, 370406, 370481, 370500, 370501, 370502,            370503, 370505, 370522, 370523, 370600, 370601, 370602, 370611, 370612, 370613, 370634, 370681, 370682,            370683, 370684, 370685, 370686, 370687, 370700, 370701, 370702, 370703, 370704, 370705, 370724, 370725,            370781, 370782, 370783, 370784, 370785, 370786, 370800, 370801, 370811, 370812, 370826, 370827, 370828,            370829, 370830, 370831, 370832, 370881, 370883, 370900, 370901, 370902, 370911, 370921, 370923, 370982,            370983, 371000, 371001, 371002, 371003, 371082, 371083, 371100, 371101, 371102, 371103, 371121, 371122,            371200, 371201, 371202, 371203, 371300, 371301, 371302, 371311, 371312, 371321, 371322, 371323, 371324,            371325, 371326, 371327, 371328, 371329, 371400, 371401, 371402, 371403, 371422, 371423, 371424, 371425,            371426, 371427, 371428, 371481, 371482, 371500, 371501, 371502, 371521, 371522, 371523, 371524, 371525,            371526, 371581, 371600, 371601, 371602, 371603, 371621, 371622, 371623, 371625, 371626, 371700, 371701,            371702, 371721, 371722, 371723, 371724, 371725, 371726, 371703, 371728, 410100, 410101, 410102, 410103,            410104, 410105, 410106, 410108, 410122, 410181, 410182, 410183, 410184, 410185, 410200, 410201, 410202,            410203, 410204, 410205, 410212, 410221, 410222, 410223, 410225, 410300, 410301, 410302, 410303, 410304,            410305, 410306, 410311, 410322, 410323, 410324, 410325, 410326, 410327, 410328, 410329, 410381, 410400,            410401, 410402, 410403, 410404, 410411, 410421, 410422, 410423, 410425, 410481, 410482, 410500, 410501,            410502, 410503, 410505, 410506, 410522, 410523, 410526, 410527, 410581, 410600, 410601, 410602, 410603,            410611, 410621, 410622, 410700, 410701, 410702, 410703, 410704, 410711, 410721, 410724, 410725, 410726,            410727, 410728, 410781, 410782, 410800, 410801, 410802, 410803, 410804, 410811, 410821, 410822, 410823,            410825, 410882, 410883, 410900, 410901, 410902, 410922, 410923, 410926, 410927, 410928, 411000, 411001,            411002, 411003, 411024, 411025, 411081, 411082, 411100, 411101, 411102, 411103, 411104, 411121, 411122,            411200, 411201, 411202, 411203, 411221, 411224, 411281, 411282, 411300, 411301, 411302, 411303, 411321,            411322, 411323, 411324, 411325, 411326, 411327, 411328, 411329, 411330, 411381, 411400, 411401, 411402,            411403, 411421, 411422, 411423, 411424, 411425, 411426, 411481, 411500, 411501, 411502, 411503, 411521,            411522, 411523, 411524, 411525, 411526, 411527, 411528, 411600, 411601, 411602, 411621, 411622, 411623,            411624, 411625, 411626, 411627, 411628, 411681, 411700, 411701, 411702, 411721, 411722, 411723, 411724,            411725, 411726, 411727, 411728, 411729, 419001, 420100, 420101, 420102, 420103, 420104, 420105, 420106,            420107, 420111, 420112, 420113, 420114, 420115, 420116, 420117, 420200, 420201, 420202, 420203, 420204,            420205, 420222, 420281, 420300, 420301, 420302, 420303, 420304, 420322, 420323, 420324, 420325, 420381,            420500, 420501, 420502, 420503, 420504, 420505, 420506, 420525, 420526, 420527, 420528, 420529, 420581,            420582, 420583, 420600, 420601, 420602, 420606, 420607, 420624, 420625, 420626, 420682, 420683, 420684,            420700, 420701, 420702, 420703, 420704, 420800, 420801, 420802, 420804, 420821, 420822, 420881, 420900,            420901, 420902, 420921, 420922, 420923, 420981, 420982, 420984, 421000, 421001, 421002, 421003, 421022,            421023, 421024, 421081, 421083, 421087, 421100, 421101, 421102, 421121, 421122, 421123, 421124, 421125,            421126, 421127, 421181, 421182, 421200, 421201, 421202, 421221, 421222, 421223, 421224, 421281, 421300,            421301, 421303, 421321, 421381, 422800, 422801, 422802, 422822, 422823, 422825, 422826, 422827, 422828,            429004, 429005, 429006, 429021, 430100, 430101, 430102, 430103, 430104, 430105, 430111, 430112, 430121,            430124, 430181, 430200, 430201, 430202, 430203, 430204, 430211, 430221, 430223, 430224, 430225, 430281,            430300, 430301, 430302, 430304, 430321, 430381, 430382, 430400, 430401, 430405, 430406, 430407, 430408,            430412, 430421, 430422, 430423, 430424, 430426, 430481, 430482, 430500, 430501, 430502, 430503, 430511,            430521, 430522, 430523, 430524, 430525, 430527, 430528, 430529, 430581, 430600, 430601, 430602, 430603,            430611, 430621, 430623, 430624, 430626, 430681, 430682, 430700, 430701, 430702, 430703, 430721, 430722,            430723, 430724, 430725, 430726, 430781, 430800, 430801, 430802, 430811, 430821, 430822, 430900, 430901,            430902, 430903, 430921, 430922, 430923, 430981, 431000, 431001, 431002, 431003, 431021, 431022, 431023,            431024, 431025, 431026, 431027, 431028, 431081, 431100, 431101, 431102, 431103, 431121, 431122, 431123,            431124, 431125, 431126, 431127, 431128, 431129, 431200, 431201, 431202, 431221, 431222, 431223, 431224,            431225, 431226, 431227, 431228, 431229, 431230, 431281, 431300, 431301, 431302, 431321, 431322, 431381,            431382, 433100, 433101, 433122, 433123, 433124, 433125, 433126, 433127, 433130, 440100, 440101, 440103,            440104, 440105, 440106, 440111, 440112, 440113, 440114, 440115, 440117, 440118, 440200, 440201, 440203,            440204, 440205, 440222, 440224, 440229, 440232, 440233, 440281, 440282, 440300, 440301, 440303, 440304,            440305, 440306, 440307, 440308, 440309, 440310, 440400, 440401, 440402, 440403, 440404, 440500, 440501,            440507, 440511, 440512, 440513, 440514, 440515, 440523, 440600, 440601, 440604, 440605, 440606, 440607,            440608, 440700, 440701, 440703, 440704, 440705, 440781, 440783, 440784, 440785, 440800, 440801, 440802,            440803, 440804, 440811, 440823, 440825, 440881, 440882, 440883, 440900, 440901, 440902, 440904, 440981,            440982, 440983, 441200, 441201, 441202, 441203, 441223, 441224, 441225, 441226, 441204, 441284, 441300,            441301, 441302, 441303, 441322, 441323, 441324, 441400, 441401, 441402, 441403, 441422, 441423, 441424,            441426, 441427, 441481, 441500, 441501, 441502, 441521, 441523, 441581, 441600, 441601, 441602, 441621,            441622, 441623, 441624, 441625, 441700, 441701, 441702, 441704, 441721, 441781, 441800, 441801, 441802,            441803, 441821, 441823, 441825, 441826, 441881, 441882, 441900, 442000, 445100, 445101, 445102, 445103,            445122, 445200, 445201, 445202, 445203, 445222, 445224, 445281, 445300, 445301, 445302, 445303, 445321,            445322, 445381, 450100, 450101, 450102, 450103, 450105, 450107, 450108, 450109, 450110, 450123, 450124,            450125, 450126, 450127, 450200, 450201, 450202, 450203, 450204, 450205, 450206, 450222, 450223, 450224,            450225, 450226, 450300, 450301, 450302, 450303, 450304, 450305, 450311, 450312, 450321, 450323, 450324,            450325, 450326, 450327, 450328, 450329, 450330, 450331, 450332, 450400, 450401, 450403, 450405, 450406,            450421, 450422, 450423, 450481, 450500, 450501, 450502, 450503, 450512, 450521, 450600, 450601, 450602,            450603, 450621, 450681, 450700, 450701, 450702, 450703, 450721, 450722, 450800, 450801, 450802, 450803,            450804, 450821, 450881, 450900, 450901, 450902, 450903, 450921, 450922, 450923, 450924, 450981, 451000,            451001, 451002, 451021, 451022, 451023, 451024, 451081, 451026, 451027, 451028, 451029, 451030, 451031,            451100, 451101, 451102, 451103, 451121, 451122, 451123, 451200, 451201, 451202, 451221, 451222, 451223,            451224, 451225, 451226, 451227, 451228, 451229, 451203, 451300, 451301, 451302, 451321, 451322, 451323,            451324, 451381, 451400, 451401, 451402, 451421, 451422, 451423, 451424, 451425, 451481, 460100, 460101,            460105, 460106, 460107, 460108, 460200, 460201, 460202, 460203, 460204, 460205, 460300, 460301, 460321,            460322, 460323, 460400, 469001, 469002, 469005, 469006, 469007, 469021, 469022, 469023, 469024, 469025,            469026, 469027, 469028, 469029, 469030, 500000, 500100, 500101, 500102, 500103, 500104, 500105, 500106,            500107, 500108, 500109, 500110, 500111, 500112, 500113, 500114, 500115, 500116, 500117, 500118, 500119,            500120, 500151, 500152, 500153, 500154, 500155, 500156, 500200, 500229, 500230, 500231, 500233, 500235,            500236, 500237, 500238, 500240, 500241, 500242, 500243, 510100, 510101, 510104, 510105, 510106, 510107,            510108, 510112, 510113, 510114, 510115, 510121, 510116, 510117, 510129, 510131, 510132, 510185, 510181,            510182, 510183, 510184, 510300, 510301, 510302, 510303, 510304, 510311, 510321, 510322, 510400, 510401,            510402, 510403, 510411, 510421, 510422, 510500, 510501, 510502, 510503, 510504, 510521, 510522, 510524,            510525, 510600, 510601, 510603, 510623, 510626, 510681, 510682, 510683, 510700, 510701, 510703, 510704,            510722, 510723, 510705, 510725, 510726, 510727, 510781, 510800, 510801, 510802, 510811, 510812, 510821,            510822, 510823, 510824, 510900, 510901, 510903, 510904, 510921, 510922, 510923, 511000, 511001, 511002,            511011, 511024, 511025, 511028, 511100, 511101, 511102, 511111, 511112, 511113, 511123, 511124, 511126,            511129, 511132, 511133, 511181, 511300, 511301, 511302, 511303, 511304, 511321, 511322, 511323, 511324,            511325, 511381, 511400, 511401, 511402, 511403, 511421, 511423, 511424, 511425, 511500, 511501, 511502,            511503, 511521, 511523, 511524, 511525, 511526, 511527, 511528, 511529, 511600, 511601, 511602, 511603,            511621, 511622, 511623, 511681, 511700, 511701, 511702, 511703, 511722, 511723, 511724, 511725, 511781,            511800, 511801, 511802, 511803, 511822, 511823, 511824, 511825, 511826, 511827, 511900, 511901, 511902,            511903, 511921, 511922, 511923, 512000, 512001, 512002, 512021, 512022, 513200, 513221, 513222, 513223,            513224, 513225, 513226, 513227, 513228, 513201, 513230, 513231, 513232, 513233, 513300, 513301, 513322,            513323, 513324, 513325, 513326, 513327, 513328, 513329, 513330, 513331, 513332, 513333, 513334, 513335,            513336, 513337, 513338, 513400, 513401, 513422, 513423, 513424, 513425, 513426, 513427, 513428, 513429,            513430, 513431, 513432, 513433, 513434, 513435, 513436, 513437, 520100, 520101, 520102, 520103, 520111,            520112, 520113, 520115, 520121, 520122, 520123, 520181, 520200, 520201, 520203, 520221, 520222, 520300,            520301, 520302, 520303, 520304, 520322, 520323, 520324, 520325, 520326, 520327, 520328, 520329, 520330,            520381, 520382, 520400, 520401, 520402, 520403, 520422, 520423, 520424, 520425, 520500, 520502, 520521,            520522, 520523, 520524, 520525, 520526, 520527, 520600, 520602, 520603, 520621, 520622, 520623, 520624,            520625, 520626, 520627, 520628, 522300, 522301, 522322, 522323, 522324, 522325, 522326, 522327, 522328,            522600, 522601, 522622, 522623, 522624, 522625, 522626, 522627, 522628, 522629, 522630, 522631, 522632,            522633, 522634, 522635, 522636, 522700, 522701, 522702, 522722, 522723, 522725, 522726, 522727, 522728,            522729, 522730, 522731, 522732, 530100, 530101, 530102, 530103, 530111, 530112, 530113, 530114, 530115,            530124, 530125, 530126, 530127, 530128, 530129, 530181, 530300, 530301, 530302, 530321, 530322, 530323,            530324, 530325, 530326, 530303, 530381, 530400, 530401, 530402, 530403, 530422, 530423, 530424, 530425,            530426, 530427, 530428, 530500, 530501, 530502, 530521, 530581, 530523, 530524, 530600, 530601, 530602,            530621, 530622, 530623, 530624, 530625, 530626, 530627, 530628, 530629, 530630, 530700, 530701, 530702,            530721, 530722, 530723, 530724, 530800, 530801, 530802, 530821, 530822, 530823, 530824, 530825, 530826,            530827, 530828, 530829, 530900, 530901, 530902, 530921, 530922, 530923, 530924, 530925, 530926, 530927,            532300, 532301, 532322, 532323, 532324, 532325, 532326, 532327, 532328, 532329, 532331, 532500, 532501,            532502, 532503, 532504, 532523, 532524, 532525, 532527, 532528, 532529, 532530, 532531, 532532, 532600,            532601, 532622, 532623, 532624, 532625, 532626, 532627, 532628, 532800, 532801, 532822, 532823, 532900,            532901, 532922, 532923, 532924, 532925, 532926, 532927, 532928, 532929, 532930, 532931, 532932, 533100,            533102, 533103, 533122, 533123, 533124, 533300, 533301, 533323, 533324, 533325, 533400, 533401, 533422,            533423, 540100, 540101, 540102, 540121, 540122, 540123, 540124, 540103, 540126, 540127, 540200, 540202,            540221, 540222, 540223, 540224, 540225, 540226, 540227, 540228, 540229, 540230, 540231, 540232, 540233,            540234, 540235, 540236, 540237, 540300, 540302, 540321, 540322, 540323, 540324, 540325, 540326, 540327,            540328, 540329, 540330, 540500, 540502, 540521, 540522, 540523, 540524, 540525, 540526, 540527, 540528,            540529, 540530, 540531, 542400, 542421, 542422, 542423, 542424, 542425, 542426, 542427, 542428, 542429,            542430, 542431, 542500, 542521, 542522, 542523, 542524, 542525, 542526, 542527, 540400, 540402, 540421,            540422, 540423, 540424, 540425, 540426, 610100, 610101, 610102, 610103, 610104, 610111, 610112, 610113,            610114, 610115, 610116, 610117, 610122, 610124, 610118, 610200, 610201, 610202, 610203, 610204, 610222,            610300, 610301, 610302, 610303, 610304, 610322, 610323, 610324, 610326, 610327, 610328, 610329, 610330,            610331, 610400, 610401, 610402, 610403, 610404, 610422, 610423, 610424, 610425, 610426, 610427, 610428,            610429, 610430, 610431, 610481, 610500, 610501, 610502, 610503, 610522, 610523, 610524, 610525, 610526,            610527, 610528, 610581, 610582, 610600, 610601, 610602, 610621, 610622, 610623, 610603, 610625, 610626,            610627, 610628, 610629, 610630, 610631, 610632, 610700, 610701, 610702, 610721, 610722, 610723, 610724,            610725, 610726, 610727, 610728, 610729, 610730, 610800, 610801, 610802, 610881, 610822, 610803, 610824,            610825, 610826, 610827, 610828, 610829, 610830, 610831, 610900, 610901, 610902, 610921, 610922, 610923,            610924, 610925, 610926, 610927, 610928, 610929, 611000, 611001, 611002, 611021, 611022, 611023, 611024,            611025, 611026, 620100, 620101, 620102, 620103, 620104, 620105, 620111, 620121, 620122, 620123, 620200,            620201, 620300, 620301, 620302, 620321, 620400, 620401, 620402, 620403, 620421, 620422, 620423, 620500,            620501, 620502, 620503, 620521, 620522, 620523, 620524, 620525, 620600, 620601, 620602, 620621, 620622,            620623, 620700, 620701, 620702, 620721, 620722, 620723, 620724, 620725, 620800, 620801, 620802, 620821,            620822, 620823, 620824, 620825, 620826, 620900, 620901, 620902, 620921, 620922, 620923, 620924, 620981,            620982, 621000, 621001, 621002, 621021, 621022, 621023, 621024, 621025, 621026, 621027, 621100, 621101,            621102, 621121, 621122, 621123, 621124, 621125, 621126, 621200, 621201, 621202, 621221, 621222, 621223,            621224, 621225, 621226, 621227, 621228, 622900, 622901, 622921, 622922, 622923, 622924, 622925, 622926,            622927, 623000, 623001, 623021, 623022, 623023, 623024, 623025, 623026, 623027, 630100, 630101, 630102,            630103, 630104, 630105, 630121, 630122, 630123, 630200, 630202, 630203, 630222, 630223, 630224, 630225,            632200, 632221, 632222, 632223, 632224, 632300, 632321, 632322, 632323, 632324, 632500, 632521, 632522,            632523, 632524, 632525, 632600, 632621, 632622, 632623, 632624, 632625, 632626, 632700, 632701, 632722,            632723, 632724, 632725, 632726, 632800, 632801, 632802, 632821, 632822, 632823, 632825, 640100, 640101,            640104, 640105, 640106, 640121, 640122, 640181, 640200, 640201, 640202, 640205, 640221, 640300, 640301,            640302, 640303, 640323, 640324, 640381, 640400, 640401, 640402, 640422, 640423, 640424, 640425, 640500,            640501, 640502, 640521, 640522, 650100, 650101, 650102, 650103, 650104, 650105, 650106, 650107, 650109,            650121, 650200, 650201, 650202, 650203, 650204, 650205, 650400, 650402, 650421, 650422, 650500, 650502,            650521, 650522, 652300, 652301, 652302, 652323, 652324, 652325, 652327, 652328, 652700, 652701, 652702,            652722, 652723, 652800, 652801, 652822, 652823, 652824, 652825, 652826, 652827, 652828, 652829, 652900,            652901, 652922, 652923, 652924, 652925, 652926, 652927, 652928, 652929, 653000, 653001, 653022, 653023,            653024, 653100, 653101, 653121, 653122, 653123, 653124, 653125, 653126, 653127, 653128, 653129, 653130,            653131, 653200, 653201, 653221, 653222, 653223, 653224, 653225, 653226, 653227, 654000, 654002, 654003,            654004, 654021, 654022, 654023, 654024, 654025, 654026, 654027, 654028, 654200, 654201, 654202, 654221,            654223, 654224, 654225, 654226, 654300, 654301, 654321, 654322, 654323, 654324, 654325, 654326, 659001,            659002, 659003, 659004, 659005, 659006, 659007, 659008, 659009, 710000, 810000, 810001, 810002, 810003,            810004, 810005, 810006, 810007, 810008, 810009, 810010, 810011, 810012, 810013, 810014, 810015, 810016,            810017, 810018, 820000, 820001, 820002, 820003, 820004, 820005, 820006, 820007, 820008, 900000, 442101]# 种类只需要最大类和无分类搜索type_ids = ['']q = Queue()# 初始化日志文件logger = init_logger("../data/log.txt")# 链接MongoDB数据库conn = MongoClient("localhost", 27017)db = conn.amap_data  # 连接mydb数据库，没有则自动创建class Amap_spider():    def __init__(self, type_id, city, keyword, set_name, judge_words=None):        """        初始化会获取总页数，连接MongoDB数据库        :param keyword:  关键词        :param type_id:  查询POI类型,即分类,可查询poi类型编码excel        :param city:   查询城市，可选值：城市中文、中文全拼、citycode、adcode        :param set_name:   MongoDB集合名字，最好用brand_id        :param judge_words:   过滤关键词，["",""]，有这些关键词就加入数据库        """        self.judge_words = judge_words        self.keywords = keyword        self.type_id = type_id        self.city = city        self.url = "http://restapi.amap.com/v3/place/text"        self.data = {            "key": "5f2e9ed810bca7a99abc98f3808afce5",            "keywords": keyword,            "types": type_id,  # 查询POI类型            "city": city,  # 查询城市            "citylimit": True,  # 仅返回指定城市数据            "children": 1,            "offset": 20,            "page": 1,  # 最大翻页数100            "extensions": "all",        }        self.page = 1        self.total_count = 0.1  # 记录总条数        self.get_data(1)  # 初始化页码数        self.page_num = self.total_count // 20 + 2 if self.total_count % 20 != 0 else self.total_count // 20 + 1        self.my_set = eval('db.{}'.format(set_name))  # 使用amap_set集合，没有则自动创建        # 先打印信息,每爬一个新地方就标记        text = "初始化成功，关键词:{}，城市编号:{}，类型编号:{}，共有{}页，共{}条数据".format(keyword, city, type_id, self.page_num - 1,                                                                  self.total_count)        print(text)        logger.info(text)    @retry(ConnectionError, 4)    def get_data(self, page=1):        """        输入页码,获取并储存每一天数据        :param page: 页码        :return:        """        print("正在解析,关键词:{},城市编号:{},类型编号:{},页码:{}".format(self.keywords, self.city, self.type_id, page))        self.data["page"] = page        response = requests.get(url=self.url, params=self.data)        j_response = json.loads(response.text)        if self.total_count == 0.1:            self.total_count = int(j_response["count"])  # 如果是第一次爬取新的地方，则赋值总条数            return        self.save_to_mongo(j_response["pois"])    def save_to_mongo(self, pois):        """        将列表中的每条数据更新加入数据库        :param pois: [{}{}{}]        :return: None        """        for poi in pois:            if self.judge_words:  # 如果有判断词                judgment = False                for j in self.judge_words:                    judgment = (j in poi["name"]) | judgment            else:  # 没有判断词                judgment = True            if judgment:                _id = poi["id"]                # 更新每一条数据                self.my_set.update({"id": _id}, {"$set": poi}, upsert=True)                # self.my_set.insert(poi)        print("有：", len(pois), "条数据")        return None    def get_each_data(self):        for i in range(1, self.page_num):            self.get_data(i)def amap_save(keywords, set_name, judge_words):    for addr_id in addr_ids:  # 遍历市区id        for type_id in type_ids:  # 遍历类型            for keyword in keywords:                q.put((type_id, addr_id, keyword, set_name, judge_words))  # 加入队列    time.sleep(1)    # 启用多线程    ths = [Thread(target=get_data) for _ in range(8)]    for th in ths:        th.start()    for th in ths:        th.join()def get_data():    while not q.empty():        type_id, addr_id, keyword, set_name, judge_words = q.get()        try:  # 如果错误            ampa = Amap_spider(type_id, addr_id, keyword, set_name, judge_words)            ampa.get_each_data()        except Exception as e:            logger.error("类型:{}，地址:{}，错误，错误代码：".format(e, addr_ids))            ampa = Amap_spider(type_id, addr_id, keyword, set_name, judge_words)            ampa.get_each_data()            time.sleep(0.1)def main():    """关键字可以是多个"""    amap_save(["兰花草整体家居", '兰花草整体软装', '兰花草布艺'], "d0112", ["兰花草"])if __name__ == '__main__':    main()