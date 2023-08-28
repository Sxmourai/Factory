use bevy::{prelude::*, input::common_conditions::input_toggle_active, render::camera::ScalingMode};
use bevy_inspector_egui::quick::WorldInspectorPlugin;

use crate::{player::{player_movement, Player}, ui::{Money, game_ui}};

pub fn get_window_plugin() -> WindowPlugin {
    WindowPlugin {
        primary_window: Some(Window {
        title: "Factory game".into(),
        resolution: (640.0, 480.0).into(),
        resizable:false,
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
            WorldInspectorPlugin::default().run_if(input_toggle_active(true, KeyCode::Escape))
        ))
        .add_systems(Startup, setup)
        .add_systems(Startup, game_ui)
        .add_systems(Update, player_movement)
        .insert_resource(Money(100.0))
        ;
    }
}


fn setup(mut commands: Commands, assets: Res<AssetServer>) {
    let mut camera = Camera2dBundle::default();
    camera.projection.scaling_mode = ScalingMode::AutoMin { min_width: 256.0, min_height: 144.0 };
    commands.spawn(camera);

    let texture = assets.load("tile.png");

    commands.spawn((SpriteBundle {
        sprite: Sprite {
            custom_size: Some(Vec2::new(100.0, 100.0)),
            ..default()
        },
        texture,
        ..default()
    },
    Player {speed:100.0, pos: Vec2::ZERO},
    ));
}