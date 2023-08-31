

use egui_macroquad::egui::epaint::RectShape;
use egui_macroquad::egui::{Label, Context, Slider, Widget, Shape, Rounding, Color32, Stroke, Pos2};
use macroquad::ui::{root_ui, Skin};
use macroquad::prelude::*;

pub fn draw_ui() {
    let energy = 5;
    let max_energy = 1000;
    egui_macroquad::ui(|egui_ctx| {
        egui_macroquad::egui::CentralPanel::default().show(egui_ctx, |ui| {
            ui.label("hi");
            ui.horizontal(|h| {
                h.
                Shape::Rect(RectShape {rect: egui_macroquad::egui::Rect {
                        min: Pos2::new(0.,0.),
                        max: Pos2::new(32., 32.), 
                    },
                    rounding: Rounding::default(),
                    fill: Color32::from_rgb(255,0,0), 
                    stroke: Stroke::new(32., Color32::from_rgb(0,0,255)),
                });
                // h.add();
            });
        });
        // egui_macroquad::egui::Window::new("egui ❤ macroquad").show(egui_ctx, |ui| {
        //     ui.colored_label(egui_macroquad::egui::Color32::WHITE, "Test");
        //     ui.add(egui_macroquad::egui::TextEdit::singleline(&mut "ku").text_color(egui_macroquad::egui::Color32::RED));
        // });
    });

    
    // root_ui().horizontal(|ui| {
        //     let name_label = ui.label("Your name: ");
        //     ui.text_edit_singleline(&mut "Hi")
        //         .labelled_by(name_label.id);
        // });
        // root_ui().add(egui::Slider::new(&mut 10, 0..=120).text("age"));
        // if root_ui().button("Click each year").clicked() {
            //     print!("A");
            // }
            // root_ui().label(format!("Hello"));
            
    egui_macroquad::draw();
}


// use bevy::prelude::*;

// use crate::player::Player;

// #[derive(Resource)]
// pub struct Money(pub f32);

// #[derive(Component)]
// pub struct MoneyText;

// pub struct UIPlugin;
// impl Plugin for UIPlugin {
//     fn build(&self, app: &mut App) {
//         app.add_systems(Startup, game_ui)
//         ;
//     }
// }


// pub fn game_ui(mut commands: Commands, assets: Res<AssetServer>) {
//     commands.spawn((NodeBundle {
//         style: Style {
//             width: Val::Percent(80.0),
//             height: Val::Percent(15.0),
//             align_items: AlignItems::Center,
//             padding: UiRect::all(Val::Px(10.0)),
//             justify_content: JustifyContent::Center,
//             top: Val::Percent(85.0),
//             position_type: PositionType::Absolute,
//             ..default()
//         },
//         ..default()
//     }, Name::new("Hotbar"))).with_children(|commands| {
//         commands.spawn(ButtonBundle {
//             style: Style {
//                 width: Val::Px(64.0),
//                 height: Val::Px(64.0),
//                 ..default()
//             },
//             background_color: Color::BEIGE.into(),
//             image: UiImage::new(assets.load("construct.png")),
//             interaction: Interaction::Pressed,
//             ..default()
//         });
//         commands.spawn(ButtonBundle {
//             style: Style {
//                 width: Val::Px(64.0),
//                 height: Val::Px(64.0),
//                 ..default()
//             },
//             background_color: Color::BEIGE.into(),
//             image: UiImage::new(assets.load("deconstruct.png")),
//             interaction: Interaction::Pressed,
//             ..default()
//         });
//     });

//     commands.spawn((
//         NodeBundle {
//             style: Style {
//                 width: Val::Percent(100.0),
//                 height: Val::Percent(10.0),
//                 align_items: AlignItems::Center,
//                 padding: UiRect::all(Val::Px(10.0)),
//                 justify_content: JustifyContent::SpaceBetween,
//                 ..default()
//             },
//             background_color: Color::rgb(0.2, 0.2, 0.2).into(),
//             ..default()
//         },
//         Name::new("Status bar")
//     )).with_children(|commands| {
//         commands.spawn((
//             TextBundle {
//                 text: Text::from_section("Money", TextStyle { font_size: 16.0, ..default() }),
//                 ..default()
//             },
//             MoneyText
//         ));
//         commands.spawn(
//             TextBundle {
//                 text: Text::from_section("Health", TextStyle { font_size: 16.0, ..default() }),
//                 ..default()
//             }
//         );
//         commands.spawn(
//             TextBundle {
//                 text: Text::from_section("Energy", TextStyle { font_size: 16.0, ..default() }),
//                 ..default()
//             }
//         );
//     });
// }

// pub fn update_ui(
//     mut texts: Query<&mut Text>, 
//     player: Query<&Player>,
//     mut interaction_query: Query<(
//             &Interaction,
//             &mut BackgroundColor,
//             &mut BorderColor,
//             &Children,),
//         (Changed<Interaction>, With<Button>),>,) {
//     for mut text in &mut texts {
//         if text.sections[0].value.contains("Money") {
//             text.sections[0].value = format!("Money: ${:?}", player.single().money);
//         }
//         else if text.sections[0].value.contains("Health") {
//             text.sections[0].value = format!("Health: {:?}", player.single().health);
//         }
//         else if text.sections[0].value.contains("Energy") {
//             text.sections[0].value = format!("Energy: {:?}", player.single().energy);
//         }
//     }
    
//     for (interaction, mut color, mut border_color, children) in &mut interaction_query {
//         match *interaction {
//             Interaction::Pressed => {
//             }
//             _ => {}
//         }
//     }
// }
