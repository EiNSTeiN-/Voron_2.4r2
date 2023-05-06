from braceexpand import braceexpand
from boltons import fileutils
import shutil, shlex
import os
import re

slicer_bin = '/home/einstein/PrusaSlicer-2.5.0+linux-x64-GTK3-202209060725.AppImage'
slicer_options = '--export-stl --ensure-on-bed --repair --output %s %s %s'

copies = [
	dict(
        dir = "deps/Voron2.4/STLs",
        files = [
            "Z_Drive/z_drive_main_{a,b}_x2.stl",
            "Z_Drive/z_drive_retainer_{a,b}_x2.stl",
            "Z_Drive/z_motor_mount_{a,b}_x2.stl",
            "Z_Drive/[a]_belt_tensioner_{a,b}_x2.stl",
            "Z_Drive/[a]_z_drive_baseplate_{a,b}_x2.stl",
        ],
        output = "STLs/Z_Drive"
    ),
	dict(
        dir = "deps/Voron2.4/STLs",
        files = [
            "Z_Idlers/z_tensioner_bracket_{a,b}_x2.stl",
	        "Z_Idlers/[a]_z_tensioner_x4_9mm.stl",
        ],
        output = "STLs/Z_Idlers"
    ),
	dict(
        dir = "deps/Voron2.4/STLs",
        files = [
            "Gantry/z_chain_{guide,bottom_anchor}.stl",
            "Gantry/[a]_z_belt_clip_{lower,upper}_x4.stl",
            "Gantry/AB_Drive_Units/{a,b}_drive_frame_{lower,upper}.stl",
            "Gantry/AB_Drive_Units/[a]_z_chain_retainer_bracket_x2.stl",
            "Gantry/Front_Idlers/front_idler_{left,right}_{lower,upper}.stl",
            "Gantry/Front_Idlers/[a]_tensioner_{left,right}.stl",
            "Gantry/X_Axis/XY_Joints/xy_joint_{left,right}_{lower,upper}_MGN12.stl",
            "Gantry/Z_Joints/z_joint_{lower,upper}_x4.stl",
        ],
        output = "STLs/Gantry"
    ),
	dict(
        dir = "deps/Voron2.4/STLs",
        files = [
            "Tools/MGN{9,12}_rail_guide_x2.stl",
            "Tools/pulley_jig.stl",
        ],
        output = "STLs/Tools"
    ),
	dict(
        dir = "deps/Voron2.4/STLs",
        files = [
            "Spool_Management/spool_holder.stl",
        ],
        output = "STLs/Accessories"
    ),
	dict(
        dir = "deps/Voron2.4/STLs",
        files = [
            "Skirts/350/front_skirt_{a,b}_350.stl",
            "Skirts/350/rear_center_skirt_350.stl",
            "Skirts/350/side_skirt_{a,b}_350_x2.stl",
            "Skirts/keystone_panel.stl",
            "Skirts/mini12864_case_{front,rear}.stl",
            "Skirts/power_inlet_filtered.stl",
            "Skirts/side_fan_support_x2.STL",
            "Skirts/[a]_belt_guard_{a,b}_x2.stl",
            "Skirts/[a]_btt_knob_light_shield.stl",
            "Skirts/[a]_fan_grill_{a,b,retainer}_x2.stl",
            "Skirts/[a]_mini12864_case_{front_insert,hinge}.stl",
        ],
        output = "STLs/Skirts"
    ),
	dict(
        dir = "deps/Voron2.4/STLs",
        files = [
            "Panel_Mounting/Front_Doors/{door_hinge_x6,handle_a_x2,handle_b_x2,latch_x2}.stl",
            "Panel_Mounting/{bottom_panel_clip_x4,bottom_panel_hinge_x2}.stl",
            "Panel_Mounting/{corner_panel_clip_4mm_x8,corner_panel_clip_6mm_x8}.stl",
            "Panel_Mounting/{midspan_panel_clip_4mm_x7,midspan_panel_clip_6mm_x8}.stl",
            "Panel_Mounting/{z_belt_cover_a_x2,z_belt_cover_b_x2}.stl",
            # "Exhaust_Filter/exhaust_filter_{grill,housing}.stl",
            # "Exhaust_Filter/[a]_{exhaust_fan_grill,filter_access_cover}.stl",
            "Exhaust_Filter/[a]_exhaust_filter_mount_x2.stl",
        ],
        output = "STLs/Panels"
    ),
	dict(
        dir = "deps/Voron2.4/STLs",
        files = [
            "Electronics_Bay/Controller_Mounts/Octopus_bracket_set.stl",
            "Electronics_Bay/lrs_200_psu_bracket_x2.stl",
            "Electronics_Bay/pcb_din_clip_x3.stl",
            "Electronics_Bay/PSU_stabilizer_50mm.stl",
            "Electronics_Bay/raspberrypi_bracket.stl",
            "Electronics_Bay/rs25_psu_bracket.stl",
        ],
        output = "STLs/Electronics"
    ),
	dict(
        dir = "deps/Tap/STLs",
        files = [
            # "[a]Tap_Center_r6.stl",
            # "Tap_Front_r2.stl",
            # "Tap_Magnet_{Left,Right}_r2.stl",
            "Tap_Upper_PCB_r2.stl",
        ],
        output = "STLs/tapchanger"
    ),
	dict(
        dir = "deps/tapchanger/stls",
        files = [
            "Shuttle/[a] Shuttle.stl",
            dict(file="Shuttle/[tpu] Plug-6mm.stl",rotate_x=270),
            dict(file="Stealthburner plate/Front.stl",rotate_x=90),
            "Stealthburner plate/Tap_Magnet_{Left,Right}_r2.stl",
            "Dock/Dock{Base,NozzlePad,Pivot}.stl",
            dict(file="Distribution Box/[tpu] Clip.stl_x6.stl",rotate_x=270),
            # dict(file="Distribution Box/[tpu] Strain_relief-Curved.stl",rotate_x=270),
            dict(file="Distribution Box/[tpu] Strain_relief.stl",rotate_x=270),
            dict(file="Distribution Box/Distribution_box.stl",rotate_x=270),
            dict(file="Distribution Box/Exhaust_cover.stl",rotate_x=90),
            "Strain relief/[tpu] CableFlex.stl",
            dict(file="Strain relief/StrainReliefAdapter.stl",rotate_x=180),
        ],
        output = "STLs/tapchanger"
    ),
	dict(
        dir = "deps/beacon-probe-mount-for-voron-tap-stealthburner-model_files",
        files = [
            "tap becon v6.stl",
        ],
        output = "STLs/tapchanger"
    ),
	dict(
        dir = "deps/Stealthburner/STLs",
        files = [
            "Stealthburner/[a]_stealthburner_main_body.stl",
            "Stealthburner/[c]_stealthburner_LED_diffuser.stl",
            "Stealthburner/[o]_stealthburner_LED_diffuser_mask.stl",
            "Stealthburner/[o]_stealthburner_LED_carrier.stl",
            "Stealthburner/Printheads/phaetus_dragon/stealthburner_printhead_dragon_{front,rear_cw2}.stl",
            "Stealthburner/Printheads/revo_voron/stealthburner_printhead_revo_voron_{front,rear_cw2}.stl",
            "Stealthburner/ADXL345_Mounts/sb_adxl_{mount_generic_15.5mm_c_c,washer_x2}.stl",
            "Clockwork2/motor_plate.stl",
            "Clockwork2/[a]_guidler_{a,b}.stl",
            "Clockwork2/[a]_{latch_shuttle,latch,pcb_spacer}.stl",
        ],
        output = "STLs/Extruder"
    ),
	dict(
        dir = "deps/BTT-EBB/EBB SB2240_2209 CAN/Custom Printed Parts",
        files = [
            "{cable_door,main_body}_EBB_SB.stl",
            # "CW2 Cable Bridge.STL",
            # "Printed Part for CAN Cable.stl",
        ],
        output = "STLs/Extruder"
    ),
	# dict(
    #     dir = "deps/3DO-Nozzle-Cam/printers/Voron_Stealthburner",
    #     files = [
    #         "Cam_mount_SB.stl",
    #         "PCB_mount_SB.stl",
    #     ],
    #     output = "STLs/Extruder"
    # ),
	dict(
        dir = "deps/Nevermore/V5_Duo/V2",
        files = [
            "XL_Cartridge_Lid(contributed_by_Bucknova).3mf",
            "XL_Cartridge(contributed_by_Bucknova).3mf",
            "V2_Duo_Plenum_LID.stl",
            "V2_Duo_Plenum.stl",
        ],
        output = "STLs/Nevermore"
    ),
	dict(
        dir = "deps/VoronUsers/printer_mods/chri.kai.in/Angry_CAM_USB/STL",
        files = [
            "Angry_CAM_Front_Mount.stl",
            "Front_Cover_120+.stl",
            "Rear_Cover_120+.stl",
        ],
        output = "STLs/AngryCam"
    ),
	dict(
        dir = "deps/VoronUsers/printer_mods/eddie/LED_Bar_Clip",
        files = [
            "LED_Bar_Clip_Misumi_version2.stl",
        ],
        output = "STLs/Accessories"
    ),
	dict(
        dir = "deps/voron-24-modified-bowden-tube-retainer-model_files",
        files = [
            "BowdenHolder Mod1.stl",
        ],
        output = "STLs/Accessories"
    ),
	dict(
        dir = "deps/revo-connect-holders",
        files = [
            "{0.15,0.25,0.4,0.6,0.8,1.0} Nozzle Holder.stl",
        ],
        output = "STLs/Accessories"
    ),
	dict(
        dir = "deps/revo-connect-voron-bracket/With M3 mounting hole",
        files = [
            "voron-bracket-revo-connect-6-mm-panel-m3-screw.3mf",
        ],
        output = "STLs/Accessories"
    ),
	dict(
        dir = "deps/EnragedRabbit/Carrot_Feeder/Stls",
        files = [
            dict(file="Filament blocks/Magnetic Gates/[a]_Magnetic_Gate_{0,1,2,3,4,5,6,7,8}.stl", rotate_z=90),
            "Filament blocks/Tag Plates/[a]_Tag_Plate_{0,1,2,3,4,5,6,7,8}.stl",
            dict(file="Filament blocks/Top Hat Lockers/Top_Hat_Locker_{1,2,3,4,5}_xN.stl", rotate_z=90),
            "Filament blocks/{Filament_Block_xN,Filament_Blocks_End}.stl",
            "Filament blocks/[a]_Bearing_{Insert,Insert_Feet}_x2.stl",
            "Filament blocks/[a]_{Blocks_End_Feet,Latch_xN,Top_Hat_xN}.stl",
            "Gear box/EASY BRD Option/Motor_Arm_NEMA17_EASYBRD.stl",
            "Gear box/Gear_Box_{Front,Back}.stl",
            "Gear box/[a]_{Bearing_Spacer_x2,Bottom_Panel,Knob,Logo_Plate,M4_80T_Wheel,Side_Latch_x2,Top_Panel}.stl",
            "Linear axis/{Idler_Block,Selector_Motor_Support}.stl",
            "Linear axis/[a]_{Drag_Chain_Anchor_Bottom,Motor_Lock}.stl",
            "Selector/{Belt_Tensionner,Drag_Chain_Anchor,Encoder_Cart_Left}.stl",
            "Selector/{Encoder_Cart_Right,Gate_Key,Selector_Door,TCRT_Sensor_Anchor_Off_Centered}.stl",
            "Selector/[a]_{Encoder_Locker,Selector_Cart,Servo_Arm}.stl",
            "Selector/[black]_Encoder_Cage.stl",
            "Supports/V1 or V2/[a]_Support_Feet_4mm_x4.stl",
            "Supports/Adjustable mount/[a]_Screw_x3.stl",
            "Supports/Adjustable mount/Junction_Plate_{Flat_x2,Gear_Box}.stl",
            "Supports/Adjustable mount/2020/2020_{Mount,Mount_Mirrored}.stl",
            "Supports/Adjustable mount/Option/ERCF_Easy_Brd_Bracket_Mount.stl",
        ],
        output = "STLs/EnragedRabbit/Carrot_Feeder"
    ),
	dict(
        dir = "deps/EnragedRabbit/Carrot_Feeder/Stls",
        files = [
            "Tools/Calib_Test.stl",
            "Tools/Pulley_Tool_NEMA17.stl",
        ],
        output = "STLs/EnragedRabbit/Carrot_Feeder/Tools"
    ),
	dict(
        dir = "deps/EnragedRabbit/Carrot_Patch/STLs",
        files = [
            "Handles/[a]_Handle_{0,1,2,3,4,5,6,7,8}.stl",
            "[a]_{Buffer_Wheel,Feet_x2,Latch_x3,Sliding_Arm}.stl",
            "{608_Adapter,Buffer_Axis,Buffer_Cross,Main_Body,Ptfe_Entry_M10,Spool_Arm_Long}.stl",
        ],
        output = "STLs/EnragedRabbit/Carrot_Patch"
    ),
]

for entry in copies:
    dir = entry['dir']
    output = entry['output']
    fileutils.mkdir_p(output)

    for pattern in entry['files']:
        options = []
        if type(pattern) is dict:
            if 'rotate_x' in pattern:
                options.append("--rotate-x=%s" % (pattern['rotate_x']))
            if 'rotate_y' in pattern:
                options.append("--rotate-y=%s" % (pattern['rotate_y']))
            if 'rotate_z' in pattern:
                options.append("--rotate=%s" % (pattern['rotate_z']))
            pattern = pattern['file']
        for file in braceexpand(pattern):
            basename = os.path.basename(file)
            src = f"{dir}/{file}"
            dst = f"{output}/{basename}".replace(" ", "_")
            dst = re.sub(r"\.STL$", ".stl", dst)
            dst = re.sub(r"\[a\]([^_])", r"[a]_\1", dst)

            if len(options) > 0:
                src = shlex.quote(src)
                os.system("%s %s" % (slicer_bin,  slicer_options % (dst, ' '.join(options), src)))
            else:
                shutil.copyfile(src, dst)
            print(repr(src), "=>", repr(dst))
