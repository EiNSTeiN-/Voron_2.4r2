from braceexpand import braceexpand
from boltons import fileutils
import shlex
import os
import re
import glob

slicer_bin = '/home/einstein/PrusaSlicer-2.5.0+linux-x64-GTK3-202209060725.AppImage'
options = '--export-stl --ensure-on-bed --align-xy 0,0 --center 175,175 --repair --output %s %s --merge %s'

extruder_common = [
    'STLs/Extruder/{main_body,cable_door}_EBB_SB.stl',
    'STLs/Extruder/motor_plate.stl',
    'STLs/Extruder/CW2_Cable_Bridge.stl',
    'STLs/Extruder/Printed_Part_for_CAN_Cable.stl',
    'STLs/Extruder/Printed_Part_for_CAN_Cable_v1.1_remixed.stl',
]

plates = [
    ### Extruder
    dict(
        source = [
            'STLs/Extruder/stealthburner_printhead_dragon_{front,rear_cw2}.stl',
        ] + extruder_common,
        output = "Plate/extruder_phaetus_dragon.stl"
    ),
    dict(
        source = [
            'STLs/Extruder/stealthburner_printhead_revo_voron_{front,rear_cw2}.stl',
        ] + extruder_common,
        output = "Plate/extruder_revo_voron.stl"
    ),
    dict(
        source = [
            'STLs/Extruder/stealthburner_printhead_rapido_rear_cw2.stl',
            'STLs/Extruder/Stealth_Rapido_UHF_Toolhead_Front.stl',
        ] + extruder_common,
        output = "Plate/extruder_phaetus_rapido_uhf.stl"
    ),
    dict(
        source = [
            'STLs/Extruder/sb_adxl_mount_generic_15.5mm_c_c.stl',
            { 'STLs/Extruder/sb_adxl_washer_x2.stl': 2 },
        ],
        output = "Plate/extruder_generic_adxl.stl"
    ),
    dict(
        source = [
            'STLs/Extruder/[a]_guidler_{a,b}.stl',
            'STLs/Extruder/[a]_latch_shuttle.stl',
            'STLs/Extruder/[a]_latch.stl',
            'STLs/Extruder/[a]_pcb_spacer.stl',
            'STLs/Extruder/[a]_stealthburner_main_body.stl',
        ],
        output = "Plate/extruder_[a].stl"
    ),
    dict(
        source = [
            'STLs/Extruder/[a]_guidler_{a,b}.stl',
            'STLs/Extruder/[a]_latch_shuttle.stl',
            'STLs/Extruder/[a]_latch.stl',
            'STLs/Extruder/[a]_pcb_spacer.stl',
            'STLs/Extruder/[a]_Stealth_Rapido_UHF_Front.stl',
        ],
        output = "Plate/extruder_phaetus_rapido_uhf_[a].stl"
    ),
    dict(
        source = ['STLs/Extruder/[c]_*.stl'],
        output = "Plate/extruder_[c].stl"
    ),
    dict(
        source = ['STLs/Extruder/[o]_*.stl'],
        output = "Plate/extruder_[o].stl"
    ),

    ### Gantry
    dict(
        source = [
            # 'STLs/Gantry/[a]_Tap_Center_r6.stl',
            'STLs/Gantry/[a]_tensioner_{left,right}.stl',
            { 'STLs/Gantry/[a]_z_chain_retainer_bracket_x2.stl': 2 },
            { 'STLs/Gantry/[a]_z_belt_clip_{lower,upper}_x4.stl': 4 },
        ],
        output = "Plate/gantry_[a].stl"
    ),
    dict(
        source = [
            'STLs/Gantry/{a,b}_drive_frame_{lower,upper}.stl',
        ],
        output = "Plate/gantry_ab_drive.stl"
    ),
    dict(
        source = [
            'STLs/Gantry/front_idler_{left,right}_{lower,upper}.stl',
        ],
        output = "Plate/gantry_idlers.stl"
    ),
    # dict(
    #     source = [
    #         'STLs/Gantry/Tap_*.stl',
    #         'STLs/Gantry/tap_*.stl',
    #     ],
    #     output = "Plate/gantry_tap.stl"
    # ),
    dict(
        source = [
            'STLs/Gantry/xy_joint_{left,right}_{lower,upper}_MGN12.stl',
        ],
        output = "Plate/gantry_xy_joints.stl"
    ),
    dict(
        source = [
            { 'STLs/Gantry/z_joint_{lower,upper}_x4.stl': 4 },
            'STLs/Gantry/z_chain_{bottom_anchor,guide}.stl',
        ],
        output = "Plate/gantry_z.stl"
    ),

    ### tapchanger
    dict(
        source = [
            'STLs/tapchanger/Front.stl',
            'STLs/tapchanger/Tap_Magnet_{Left,Right}_r2.stl',
            'STLs/tapchanger/Dock{Base,NozzlePad,Pivot}.stl',
            # 'STLs/tapchanger/StrainReliefAdapter.stl',
            'STLs/tapchanger/Tap_Upper_PCB_r2.stl',
        ],
        output = "Plate/tapchanger.stl"
    ),
    dict(
        source = [
            'STLs/tapchanger/[a]_Shuttle.stl',
        ],
        output = "Plate/tapchanger_[a].stl"
    ),
    dict(
        source = [
            { 'STLs/tapchanger/[tpu]_Clip.stl_x6.stl': 8 },
            'STLs/tapchanger/[tpu]_Strain_relief-Curved.stl',
            # 'STLs/tapchanger/[tpu]_Strain_relief.stl',
            'STLs/tapchanger/[tpu]_Plug-6mm.stl',
            # 'STLs/tapchanger/[tpu]_CableFlex.stl',
            
        ],
        output = "Plate/tapchanger_[tpu].stl"
    ),
    
    ### Z Axis
    dict(
        source = [
            { 'STLs/Z_Drive/z_drive_{main,retainer}_{a,b}_x2.stl': 2 },
        ],
        output = "Plate/z_axis_1.stl"
    ),
    dict(
        source = [
            { 'STLs/Z_Idlers/z_tensioner_bracket_{a,b}_x2.stl': 2 },
            { 'STLs/Z_Drive/z_motor_mount_{a,b}_x2.stl': 2 },
        ],
        output = "Plate/z_axis_2.stl"
    ),
    dict(
        source = [
            { 'STLs/Z_Drive/[a]_*_x2.stl': 2 },
            { 'STLs/Z_Idlers/[a]_*_x4_*.stl': 4 },
        ],
        output = "Plate/z_axis_[a].stl"
    ),

    ### Skirts
    dict(
        source = [
            { 'STLs/Skirts/[a]_{belt_guard,fan_grill}_{a,b}_x2.stl': 2 },
            { 'STLs/Skirts/[a]_fan_grill_retainer_x2.stl': 2 },
            'STLs/Skirts/[a]_btt_knob_light_shield.stl',
            'STLs/Skirts/[a]_mini12864_case_{front_insert,hinge}.stl',
        ],
        output = "Plate/skirts_[a].stl"
    ),
    dict(
        source = [
            'STLs/Skirts/front_skirt_{a,b}_350.stl',
            'STLs/Skirts/mini12864_case_{front,rear}.stl',
        ],
        output = "Plate/skirts_front.stl"
    ),
    dict(
        source = [
            { 'STLs/Skirts/side_skirt_{a,b}_350_x2.stl': 2},
            { 'STLs/Skirts/side_fan_support_x2.stl': 2},
        ],
        output = "Plate/skirts_side.stl"
    ),
    dict(
        source = [
            'STLs/Skirts/power_inlet_filtered.stl',
            'STLs/Skirts/rear_center_skirt_350.stl',
            'STLs/Skirts/keystone_panel.stl',
        ],
        output = "Plate/skirts_rear.stl"
    ),

    ### Panels
    dict(
        source = [
            { 'STLs/Panels/bottom_panel_clip_x4.stl': 4 },
            { 'STLs/Panels/bottom_panel_hinge_x2.stl': 2 },
        ],
        output = "Plate/panels_bottom.stl"
    ),
    dict(
        source = [
            { 'STLs/Panels/corner_panel_clip_4mm_x8.stl': 8 },
            { 'STLs/Panels/corner_panel_clip_6mm_x8.stl': 8 },
            { 'STLs/Panels/midspan_panel_clip_4mm_x7.stl': 7 },
            { 'STLs/Panels/midspan_panel_clip_6mm_x8.stl': 8 },
        ],
        output = "Plate/panels_sides.stl"
    ),
    dict(
        source = [
            { 'STLs/Panels/latch_x2.stl': 2 },
            { 'STLs/Panels/handle_{a,b}_x2.stl': 2 },
            { 'STLs/Panels/door_hinge_x6.stl': 6 },
        ],
        output = "Plate/panels_door.stl"
    ),
    dict(
        source = [
            { 'STLs/Panels/[a]_exhaust_filter_mount_x2.stl': 2 },
            # 'STLs/Panels/[a]_exhaust_fan_grill.stl',
            # 'STLs/Panels/[a]_filter_acess_cover.stl',
        ],
        output = "Plate/exhaust_[a].stl"
    ),
    dict(
        source = [
            # 'STLs/Panels/exhaust_filter_{grill,housing}.stl',
            'STLs/tapchanger/Distribution_box.stl',
            'STLs/tapchanger/Exhaust_cover.stl',
        ],
        output = "Plate/exhaust.stl"
    ),

    ### Other
    dict(
        source = [
            'STLs/Accessories/spool_holder.stl',
            'STLs/Accessories/BowdenHolder_Mod1.stl',
        ],
        output = "Plate/accessories.stl"
    ),
    dict(
        source = [
            {'STLs/Accessories/pfte_tube_magnetic_coupler.stl': 4},
        ],
        output = "Plate/accessories_pfte_tube_magnetic_couplers_[a].stl"
    ),
    dict(
        source = [
            {'STLs/Accessories/[a]_2020_Profile_Cover.stl': 18},
        ],
        output = "Plate/accessories_profile_covers_[a].stl"
    ),
    dict(
        source = [
            'STLs/Accessories/voron-bracket-revo-connect-6-mm-panel-m3-screw.3mf',
            'STLs/Accessories/*_Nozzle_Holder.stl',
        ],
        output = "Plate/accessories_revo_nozzle_holder.stl"
    ),
    dict(
        source = [
            {'STLs/Accessories/Side_Extrusion_Mount/Side_Extrusion_Mount_Feet.stl': 2},
            {'STLs/Accessories/Side_Extrusion_Mount/Misumi_2020_Endcap_80u__v1-0.stl': 2},
        ],
        output = "Plate/accessories_side_extrusion_mount_[a].stl"
    ),
    dict(
        source = [
            {'STLs/Accessories/Horizontal_Spool_Holder.stl': 2},
        ],
        output = "Plate/accessories_horizontal_spool_holder.stl"
    ),
    dict(
        source = [
            {'STLs/Accessories/Handle/handle_{inner,outer}_part.stl': 2},
        ],
        output = "Plate/accessories_handle.stl"
    ),
    dict(
        source = [
            {'STLs/Accessories/Handle/[a]_handle_middle_part.stl': 2},
        ],
        output = "Plate/accessories_handle_[a].stl"
    ),
    dict(
        source = [{ 'STLs/Accessories/LED_Bar_Clip_Misumi_version2.stl': 29 }], # fits 29 behind Z belts on 350mm printer
        output = "Plate/accessories_led_bar_clips.stl"
    ),
    dict(
        source = ['STLs/AngryCam/*.stl'],
        output = "Plate/angry_cam.stl",
        split = True
    ),
    dict(
        source = [
            { 'STLs/Electronics/lrs_200_psu_bracket_x2.stl': 2 },
            'STLs/Electronics/Octopus_bracket_set.stl',
            { 'STLs/Electronics/pcb_din_clip_x3.stl': 3 },
            'STLs/Electronics/PSU_stabilizer_50mm.stl',
            'STLs/Electronics/raspberrypi_bracket.stl',
            'STLs/Electronics/rs25_psu_bracket.stl',
        ],
        output = "Plate/electronics.stl"
    ),
    dict(
        source = ['STLs/Nevermore/V2_Duo_Plenum*.stl'],
        output = "Plate/nevermore_plenum.stl"
    ),
    dict(
        source = ['STLs/Nevermore/XL_Cartridge*.3mf'],
        output = "Plate/nevermore_xl_cartridge.stl"
    ),
    dict(
        source = ['STLs/Tools/*.stl', 'STLs/Tools/**/*.stl'],
        output = "Plate/tools.stl"
    ),

    ### Enraged Rabbit
    dict(
        source = [
            'STLs/EnragedRabbit/Carrot_Feeder/Tools/Calib_Test.stl',
            'STLs/EnragedRabbit/Carrot_Feeder/Tools/Pulley_Tool_NEMA14.stl',
            'STLs/EnragedRabbit/Carrot_Feeder/[black]_Encoder_Cage.stl',
            'STLs/EnragedRabbit/Carrot_Feeder/2020_Mount_Mirrored.stl',
            {'STLs/EnragedRabbit/Carrot_Feeder/2020_Mount.stl': 3},
            'STLs/EnragedRabbit/Carrot_Feeder/Belt_Tensionner.stl',
            'STLs/EnragedRabbit/Carrot_Feeder/Drag_Chain_Anchor.stl',
            'STLs/EnragedRabbit/Carrot_Feeder/Encoder_Cart_{Left,Right}.stl',
            'STLs/EnragedRabbit/Carrot_Feeder/ERCF_Easy_Brd_Bracket_Mount.stl',
            {'STLs/EnragedRabbit/Carrot_Feeder/Filament_Block_xN.stl': 9},
            'STLs/EnragedRabbit/Carrot_Feeder/Filament_Blocks_End.stl',
            'STLs/EnragedRabbit/Carrot_Feeder/Gate_Key.stl',
            'STLs/EnragedRabbit/Carrot_Feeder/Gear_Box_{Front,Back}.stl',
            'STLs/EnragedRabbit/Carrot_Feeder/Idler_Block.stl',
            {'STLs/EnragedRabbit/Carrot_Feeder/Junction_Plate_Flat_x2.stl': 3},
            'STLs/EnragedRabbit/Carrot_Feeder/Junction_Plate_Gear_Box.stl',
            'STLs/EnragedRabbit/Carrot_Feeder/Motor_Arm_NEMA14_EASYBRD.stl',
            'STLs/EnragedRabbit/Carrot_Feeder/Selector_Door.stl',
            'STLs/EnragedRabbit/Carrot_Feeder/Selector_Motor_Support.stl',
            'STLs/EnragedRabbit/Carrot_Feeder/TCRT_Sensor_Anchor_Off_Centered.stl',
            {'STLs/EnragedRabbit/Carrot_Feeder/Top_Hat_Locker_1_xN.stl': 9},
        ],
        output = "Plate/EnragedRabbit_CarrotFeeder.stl"
    ),
    dict(
        source = [
            {'STLs/EnragedRabbit/Carrot_Feeder/[a]_Bearing_Insert_Feet_x2.stl': 2},
            {'STLs/EnragedRabbit/Carrot_Feeder/[a]_Bearing_Insert_x2.stl': 2},
            {'STLs/EnragedRabbit/Carrot_Feeder/[a]_Bearing_Spacer_x2.stl': 2},
            'STLs/EnragedRabbit/Carrot_Feeder/[a]_Blocks_End_Feet.stl',
            'STLs/EnragedRabbit/Carrot_Feeder/[a]_Bottom_Panel.stl',
            'STLs/EnragedRabbit/Carrot_Feeder/[a]_Drag_Chain_Anchor_Bottom.stl',
            'STLs/EnragedRabbit/Carrot_Feeder/[a]_Encoder_Locker.stl',
            'STLs/EnragedRabbit/Carrot_Feeder/[a]_Knob.stl',
            {'STLs/EnragedRabbit/Carrot_Feeder/[a]_Latch_xN.stl': 9},
            'STLs/EnragedRabbit/Carrot_Feeder/[a]_Logo_Plate.stl',
            'STLs/EnragedRabbit/Carrot_Feeder/[a]_M4_80T_Wheel.stl',
            'STLs/EnragedRabbit/Carrot_Feeder/[a]_Magnetic_Gate_{0,1,2,3,4,5,6,7,8}.stl',
            'STLs/EnragedRabbit/Carrot_Feeder/[a]_Motor_Lock.stl',
            {'STLs/EnragedRabbit/Carrot_Feeder/[a]_Screw_x3.stl': 4},
            'STLs/EnragedRabbit/Carrot_Feeder/[a]_Selector_Cart.stl',
            'STLs/EnragedRabbit/Carrot_Feeder/[a]_Servo_Arm.stl',
            {'STLs/EnragedRabbit/Carrot_Feeder/[a]_Side_Latch_x2.stl': 2},
            {'STLs/EnragedRabbit/Carrot_Feeder/[a]_Support_Feet_4mm_x4.stl': 4},
            'STLs/EnragedRabbit/Carrot_Feeder/[a]_Tag_Plate_{0,1,2,3,4,5,6,7,8}.stl',
            {'STLs/EnragedRabbit/Carrot_Feeder/[a]_Top_Hat_xN.stl': 9},
            'STLs/EnragedRabbit/Carrot_Feeder/[a]_Top_Panel.stl',
        ],
        output = "Plate/EnragedRabbit_CarrotFeeder_[a].stl"
    ),
    dict(
        source = [
            'STLs/EnragedRabbit/Carrot_Patch/608_Adapter.stl',
            'STLs/EnragedRabbit/Carrot_Patch/Buffer_Axis.stl',
            'STLs/EnragedRabbit/Carrot_Patch/Ptfe_Entry_M10.stl',
            'STLs/EnragedRabbit/Carrot_Patch/Spool_Arm_Long.stl',
        ],
        output = "Plate/EnragedRabbit_CarrotPatch.stl"
    ),
    dict(
        source = [
            'STLs/EnragedRabbit/Carrot_Patch/Buffer_Cross.stl',
        ],
        output = "Plate/EnragedRabbit_CarrotPatch_Cross.stl"
    ),
    dict(
        source = [
            'STLs/EnragedRabbit/Carrot_Patch/Main_Body.stl',
        ],
        output = "Plate/EnragedRabbit_CarrotPatch_MainBody.stl"
    ),
    dict(
        source = [
            {'STLs/EnragedRabbit/Carrot_Patch/[a]_Feet_x2.stl': 2},
            'STLs/EnragedRabbit/Carrot_Patch/[a]_Buffer_Wheel.stl',
            {'STLs/EnragedRabbit/Carrot_Patch/[a]_Latch_x3.stl': 3},
            'STLs/EnragedRabbit/Carrot_Patch/[a]_Sliding_Arm.stl',
        ],
        output = "Plate/EnragedRabbit_CarrotPatch_[a].stl"
    ),
    dict(
        source = [
            'STLs/EnragedRabbit/Carrot_Patch/[a]_Handle_{0,1,2,3,4,5,6,7,8}.stl',
        ],
        output = "Plate/EnragedRabbit_CarrotPatch_Handles_[a].stl"
    ),
]

for entry in plates:
    output = entry['output']
    split = entry['split'] if 'split' in entry else False
    fileutils.mkdir_p(os.path.dirname(output))

    files = []
    for patterns in entry['source']:
        if type(patterns) is str:
            patterns = { patterns: 1 }
        
        for (pattern, count) in patterns.items():
            for expanded in braceexpand(pattern):
                escaped = re.sub('([\[\]])','[\\1]', expanded)
                globbed = [g for g in glob.iglob(escaped)]
                if len(globbed) == 0:
                    raise Exception('Glob expansion resulted in no matches: %s' % expanded)
                for file in globbed:
                    for n in range(count):
                        if not os.path.isfile(file):
                            raise Exception('File does not exist: %s' % file)
                        files.append(shlex.quote(file))

    print(repr(files), "=>", repr(output))
    os.system("%s %s" % (slicer_bin,  options % (output, '--split' if split else '', ' '.join(files))))
