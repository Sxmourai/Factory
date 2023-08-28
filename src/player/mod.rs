use bevy::prelude::*;

mod inventory;
use crate::camera::Camera;

use self::inventory::Inventory;

const BASE_ENERGY: u64 = 200_000_000;
#[derive(Component)]
pub struct Player {
    pub speed: f32,
    pub money: u64,
    pub inventory: Inventory,
    pub health: u64,
    pub energy: u64,
    pub max_energy: u64,
}
impl Player {
    pub fn spawn(mut commands: Commands, assets: Res<AssetServer>) {
        let texture = assets.load("player.png");

        commands.spawn((SpriteBundle {
            sprite: Sprite {
                custom_size: Some(Vec2::new(25.0, 25.0)),
                ..default()
            },
            texture,
            transform: Transform::from_translation(Vec3::new(0.0, 0.0, 10.0)),
            ..default()
        },
        Self {
            speed: 100.0,
            money: 0,
            health: 100_000,
            energy: BASE_ENERGY,
            max_energy: BASE_ENERGY,
            inventory: Inventory::default(),
        },
        ));
        
    }
}
pub fn player_movement(
    mut camera: Query<(&mut Transform, With<Camera>)>,
    mut player: Query<(&mut Transform, &mut Player, Without<Camera>)>,
    input: Res<Input<KeyCode>>,
    time: Res<Time>,
) {
    let (mut transform, mut player, _) = player.single_mut();
    let movement_speed = player.speed * time.delta_seconds();
    if input.pressed(KeyCode::Z) {
        transform.translation.y += movement_speed;
        player.energy -= 10;
    }
    if input.pressed(KeyCode::S) {
        transform.translation.y -= movement_speed;
        player.energy -= 10;
    }
    if input.pressed(KeyCode::D) {
        transform.translation.x += movement_speed;
        player.energy -= 10;
    }
    if input.pressed(KeyCode::Q) {
        transform.translation.x -= movement_speed;
        player.energy -= 10;
    }
    let mut camera_pos = camera.single_mut().0;
    camera_pos.translation = transform.translation;
    if player.energy < player.max_energy {player.energy += 5;}
    // let speed = camera_pos.translation.distance_squared(transform.translation)/100.0;
    // if camera_pos.translation.x > transform.translation.x {
    //     camera_pos.translation.x -= speed * movement_speed;
    // }
    // if camera_pos.translation.x < transform.translation.x {
    //     camera_pos.translation.x += speed * movement_speed;
    // }
    // if camera_pos.translation.y > transform.translation.y {
    //     camera_pos.translation.y -= speed * movement_speed;
    // }
    // if camera_pos.translation.y < transform.translation.y {
    //     camera_pos.translation.y += speed * movement_speed;
    // }
}