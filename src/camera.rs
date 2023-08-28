use bevy::{prelude::*, render::camera::ScalingMode};
#[derive(Component)]
pub struct Camera;
impl Camera {
    pub fn spawn(mut commands: Commands) {
        let mut camera = Camera2dBundle::default();
        // camera.projection.scaling_mode = ScalingMode::AutoMin { min_width: 256.0, min_height: 144.0 };
        commands.spawn((camera, Self {}));    

        commands.spawn(SpriteBundle {
            sprite: Sprite {
                color: Color::rgb(0.25, 0.25, 0.75),
                custom_size: Some(Vec2::new(50.0, 100.0)),
                ..default()
            },
            transform: Transform::from_translation(Vec3::new(0., 0., 5.)),
            ..default()
        });
    }
}