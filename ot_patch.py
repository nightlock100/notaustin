import re, sys
src = sys.argv[1]; dst = sys.argv[2]
s = open(src, encoding='utf-8', errors='surrogateescape', newline='').read()

edits = []   # (label, find, replace)

# ---- 0) simulate previous turn's OL edits if not already present (test harness only) ----
if 'case 9:{_inst.gmlpmap=(-4);break;}case 10:{_inst.gmlpmap=(-4);break;}' not in s:
    s = s.replace('case 9:{_inst.gmlpmap=gml_Script_s_get_player_by_position_from_roster(_inst,_other,_inst.gmlposition,4,gmlattack_roster);break;}case 10:{_inst.gmlpmap=gml_Script_s_get_player_by_position_from_roster(_inst,_other,_inst.gmlposition,5,gmlattack_roster);break;}',
                  'case 9:{_inst.gmlpmap=(-4);break;}case 10:{_inst.gmlpmap=(-4);break;}')
    s = s.replace('case 3:{gmlmaxpos=99;break;}case 4:{gmlmaxpos=5;break;}', 'case 3:{gmlmaxpos=99;break;}case 4:{gmlmaxpos=3;break;}')

# ---- 1) mechanical merges: OT (16) behaves like OL (5) ----
merge_ids = [62,402,626,730,922,1106,1178,1180,1190,1194,1206,1214,1218,1240,1254,1262,1286,1370,1450,1996,2010]
for n in merge_ids:
    f = 'yyCompareVal(___sw%d___,5,g_GMLMathEpsilon,false)==0' % n
    r = f + '||yyCompareVal(___sw%d___,16,g_GMLMathEpsilon,false)==0' % n
    edits.append(('merge sw%d'%n, f, r))

# ---- 2) labels ----
edits.append(('label short chain', '{___swc1343___=14;}', '{___swc1343___=14;}else if(yyCompareVal(___sw1342___,16,g_GMLMathEpsilon,false)==0){___swc1343___=15;}'))
edits.append(('label short case', 'case 14:{return "ED";break;}', 'case 14:{return "ED";break;}case 15:{return "OT";break;}'))
edits.append(('label full chain', '{___swc1347___=14;}', '{___swc1347___=14;}else if(yyCompareVal(___sw1346___,16,g_GMLMathEpsilon,false)==0){___swc1347___=15;}'))
edits.append(('label full case', 'case 14:{return "Edge Rusher";break;}', 'case 14:{return "Edge Rusher";break;}case 15:{return "Offensive Tackle";break;}'))

# ---- 3) caps: OT max 2 ----
edits.append(('cap sign', '{___swc239___=8;}switch(___swc239___){case 0:{gmlmaxpos=2;break;}', '{___swc239___=8;}else if(yyCompareVal(___sw238___,16,g_GMLMathEpsilon,false)==0){___swc239___=9;}switch(___swc239___){case 9:{gmlmaxpos=2;break;}case 0:{gmlmaxpos=2;break;}'))
edits.append(('cap breach', '{___swc409___=8;}switch(___swc409___){case 0:{gmlmaxpos=2;break;}', '{___swc409___=8;}else if(yyCompareVal(___sw408___,16,g_GMLMathEpsilon,false)==0){___swc409___=9;}switch(___swc409___){case 9:{gmlmaxpos=2;break;}case 0:{gmlmaxpos=2;break;}'))

# ---- 4) tackle spots read roster OTs ----
edits.append(('field tackles', 'case 9:{_inst.gmlpmap=(-4);break;}case 10:{_inst.gmlpmap=(-4);break;}',
 'case 9:{_inst.gmlpmap=gml_Script_s_get_player_by_position_from_roster(_inst,_other,16,1,gmlattack_roster);break;}case 10:{_inst.gmlpmap=gml_Script_s_get_player_by_position_from_roster(_inst,_other,16,2,gmlattack_roster);break;}'))

# ---- 5) generation (same spots Edge Rusher was wired into) ----
edits.append(('draft gen', 'if((yyfequal(__yy__v655.gmlpos,6))&&(yyGetBool(irandom(1)))){__yy__v655.gmlpos=15;};',
 'if((yyfequal(__yy__v655.gmlpos,6))&&(yyGetBool(irandom(1)))){__yy__v655.gmlpos=15;};if((yyfequal(__yy__v655.gmlpos,5))&&(yyGetBool(irandom(1)))){__yy__v655.gmlpos=16;};'))
edits.append(('store loop end', 'yyflessequal(gmli,15);(g_yyPrePostObject__=gmli,gmli=(g_yyPrePostObject__ instanceof Long?gmli.add(1):++gmli),g_yyPrePostObject__)){{if((gmli<=10||gmli==15)&&',
 'yyflessequal(gmli,16);(g_yyPrePostObject__=gmli,gmli=(g_yyPrePostObject__ instanceof Long?gmli.add(1):++gmli),g_yyPrePostObject__)){{if((gmli<=10||gmli==15||gmli==16)&&'))
edits.append(('required pos 1', 'gmlpos=irandom_range(1,10);if((yyfequal(gmlpos,6))&&(yyGetBool(irandom(1)))){gmlpos=15;};if(!yyGetBool(',
 'gmlpos=irandom_range(1,10);if((yyfequal(gmlpos,6))&&(yyGetBool(irandom(1)))){gmlpos=15;};if((yyfequal(gmlpos,5))&&(yyGetBool(irandom(1)))){gmlpos=16;};if(!yyGetBool('))
edits.append(('required pos 2', 'gmlpos=irandom_range(1,10);if((yyfequal(gmlpos,6))&&(yyGetBool(irandom(1)))){gmlpos=15;};if(yyfequal(gmlpos,1)){{continue;};};',
 'gmlpos=irandom_range(1,10);if((yyfequal(gmlpos,6))&&(yyGetBool(irandom(1)))){gmlpos=15;};if((yyfequal(gmlpos,5))&&(yyGetBool(irandom(1)))){gmlpos=16;};if(yyfequal(gmlpos,1)){{continue;};};'))

# ---- 6) info text + direct-equals sites ----
edits.append(('info text', 'gmlmsg="info_DB";};', 'gmlmsg="info_DB";};if(yyfequal(ds_map_find_value(yyInst(_inst,_other,97).gmlplayer_profile,"position"),16)){gmlmsg="info_OL";};'))
edits.append(('te blockers', '(yyGetBool(yyfequal(ds_map_find_value(__yy__v1059.gmlpmap,"position"),5)))',
 '((yyGetBool(yyfequal(ds_map_find_value(__yy__v1059.gmlpmap,"position"),5)))||(yyGetBool(yyfequal(ds_map_find_value(__yy__v1059.gmlpmap,"position"),16))))'))
edits.append(('tackle record', 'if(yyfnotequal(ds_map_find_value(gmlpmap,"position"),5)){{gml_Script_s_check_record(__yy__v1227,_inst,"ui_MostTacklesGame"',
 'if((yyfnotequal(ds_map_find_value(gmlpmap,"position"),5))&&(yyfnotequal(ds_map_find_value(gmlpmap,"position"),16))){{gml_Script_s_check_record(__yy__v1227,_inst,"ui_MostTacklesGame"'))

bad = False
for label, f, r in edits:
    c = s.count(f)
    if c != 1:
        print('!! %-20s matches=%d' % (label, c)); bad = True
    else:
        s = s.replace(f, r)
if not bad:
    open(dst, 'w', encoding='utf-8', errors='surrogateescape', newline='').write(s)
    print('OK: all %d edits matched exactly once' % len(edits))
