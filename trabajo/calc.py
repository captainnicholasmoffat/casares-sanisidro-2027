import math
FX=1520
window_min_wk=7*60*5   # 2100
peakf=2.0
speak=0.4; margin=1.15
hours_load=7*5*36      # 1260
hours_idle=8760-hours_load
PUE=1.5
W_load=0.575+0.100; W_idle=0.100
server_cost=10000; gpus_per_server=4
staff_cost=30000
cases={
 'a full 18713':(18713,40,18713),
 'b full 50833':(50833,40,50833),
 'c 15% of 50833':(round(0.15*50833),40,50833),
 'd Iowa 38min/yr all 50833':(50833,38/36,50833),
}
gpus_opts={'RTX5090 street':(3695,2),'RTX5090 FlashLite':(3695,3),'L40S':(10497.99,2)}
for name,(users,min_wk,denom) in cases.items():
    avg=users*min_wk/window_min_wk
    peak=avg*peakf
    streams=math.ceil(peak*speak*margin)
    print(f"\n== {name}: users={users} avg_sessions={avg:.1f} peak={peak:.0f} streams={streams}")
    for gname,(price,spg) in gpus_opts.items():
        n=math.ceil(streams/spg)
        servers=math.ceil(n/gpus_per_server)
        capex=n*price+servers*server_cost
        amort=capex/4
        kw_peak=n*W_load*PUE
        kwh=n*(W_load*hours_load+W_idle*hours_idle)*PUE
        varp=145 if kw_peak<300 else 160
        e_ars=kwh*varp + kw_peak*(19939.19+10306.30)*12 + 189126.46*12
        e_usd=e_ars/FX
        staff=(1 if n<=20 else 2 if n<=200 else 3)*staff_cost
        tot=amort+e_usd+staff
        print(f"  {gname}: GPUs={n} servers={servers} capex=${capex:,.0f} amort=${amort:,.0f} kWpeak={kw_peak:.0f} kWh={kwh:,.0f} elec=${e_usd:,.0f} staff=${staff:,.0f} TOTAL=${tot:,.0f}/yr per_student=${tot/denom:.2f} ARS {tot/denom*FX:,.0f} total ARS M {tot*FX/1e6:,.1f}")
    # rent
    for rname,ph in {'vast BR 4090':0.269,'runpod 4090':0.74}.items():
        n=math.ceil(streams/2)
        cost=n*hours_load*ph*1.10
        print(f"  RENT {rname}: GPUs={n} cost=${cost:,.0f}/yr per_student=${cost/denom:.2f}")
    # API
    api_min=users*min_wk*36*speak if 'Iowa' not in name else users*38*speak
    print(f"  API $0.50/min speaking: ${api_min*0.5:,.0f}/yr per_student=${api_min*0.5/denom:.2f}")
