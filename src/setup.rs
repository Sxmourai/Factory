use bevy::{prelude::*, input::common_conditions::input_toggle_active};
use bevy_inspector_egui::quick::WorldInspectorPlugin;

use crate::{player::{player_movement, Player}, ui::{UIPlugin, update_ui}, world::{draw_world, World}};

pub fn get_window_plugin() -> WindowPlugin {
    WindowPlugin {
        primary_window: Some(Window {
        title: "Factory game".into(),
        resolution: (640.0, 480.0).into(),
        resizable:false,
        position: WindowPosition::At(IVec2 { x: 1000, y: 400 }),
        ..default()
    }),
    ..default()
    }
}
pub struct SetupPlugin;
impl Plugin for SetupPlugin {
    fn build(&self, app: &mut App) {
        app.add_plugins((DefaultPlugins
            .set(ImagePlugin::default_nearest())
            .set(get_window_plugin()),
            WorldInspectorPlugin::default().run_if(input_toggle_active(true, KeyCode::Escape)),
            UIPlugin {},
        ))
        .add_systems(Startup, crate::camera::Camera::spawn)
        .add_systems(Startup, Player::spawn)
        .add_systems(Update, draw_world)
        .add_systems(Update, player_movement)
        .add_systems(Update, update_ui)
        .insert_resource(World::new(0))
        ;
    }
}
