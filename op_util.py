import tensorflow as tf

def Optimizer(model, LR):
    with tf.name_scope('Optimizer_w_Distillation'):
        loss_object = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        optimizer = tf.keras.optimizers.SGD(LR, .9, nesterov=True)
        
        train_loss = tf.keras.metrics.Mean(name='train_loss')
        train_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name='train_accuracy')
        test_loss = tf.keras.metrics.Mean(name='test_loss')
        test_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name='test_accuracy')
        
    @tf.function
    def training(images, labels, lr):
        with tf.GradientTape() as tape:
            predictions = model(images, training = True)
            loss = loss_object(labels, predictions)
            regularizer_loss = tf.add_n(model.losses)
            total_loss = loss + regularizer_loss
        gradients = tape.gradient(total_loss, model.trainable_variables)
        optimizer.learning_rate.assign(lr)
        optimizer.apply_gradients(zip(gradients, model.trainable_variables))
        
        train_loss(loss)
        train_accuracy(labels, predictions)
        
    @tf.function
    def validation(images, labels):
        predictions = model(images, training = False)
        loss = loss_object(labels, predictions)
        
        test_loss(loss)
        test_accuracy(labels, predictions)
    return training, train_loss, train_accuracy, validation, test_loss, test_accuracy

def Multitask_Optimizer(target_model, source_model, distill_model, LR):
    with tf.name_scope('Optimizer_w_Distillation'):
        loss_object = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        optimizer = tf.keras.optimizers.SGD(LR, .9, nesterov=True)
        
        train_loss = tf.keras.metrics.Mean(name='distill_loss')
        train_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name='train_accuracy')
        test_loss = tf.keras.metrics.Mean(name='test_loss')
        test_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name='test_accuracy')
        
    @tf.function
    def training(images, labels, lr):
        with tf.GradientTape(persistent = True) as tape:
            predictions = target_model(images, training = True)
            target_feat = getattr(target_model, distill_model.feat_name)
            source_feat = source_model.get_feat(images, distill_model.feat_name, False)
            
            loss = loss_object(labels, predictions)
            distillation_loss = distill_model(target_feat, source_feat, training = True)
            regularizer_loss = tf.add_n(target_model.losses+distill_model.losses)
            total_loss = loss + distillation_loss + regularizer_loss
            
        trained_variables = target_model.trainable_variables + distill_model.trainable_variables
        gradients = tape.gradient(total_loss, trained_variables)
        optimizer.learning_rate.assign(lr)
        optimizer.apply_gradients(zip(gradients, target_model.trainable_variables))
        
        train_loss(loss)
        train_accuracy(labels, predictions)
        
    @tf.function
    def validation(images, labels):
        predictions = target_model(images, training = False)
        loss = loss_object(labels, predictions)
        
        test_loss(loss)
        test_accuracy(labels, predictions)
    return training, train_loss, train_accuracy, validation, test_loss, test_accuracy

def Initializer_Optimizer(target_model, source_model, distill_model, LR):
    with tf.name_scope('Optimizer_w_Distillation'):
        optimizer = tf.keras.optimizers.SGD(LR, .9, nesterov=True)
        train_loss = tf.keras.metrics.Mean(name='distill_loss')
        
    @tf.function
    def training(images):
        with tf.GradientTape(persistent = True) as tape:
            target_feat = target_model.get_feat(images, distill_model.feat_name, True)
            source_feat = source_model.get_feat(images, distill_model.feat_name, False)
            distillation_loss = distill_model(target_feat, source_feat, training = True)
            regularizer_loss = tf.add_n(target_model.losses+distill_model.losses)
            
        trained_variables = target_model.trainable_variables + distill_model.trainable_variables
        gradients_dist = tape.gradient(distillation_loss, trained_variables)
        gradients_reg  = tape.gradient(regularizer_loss, trained_variables)
        
        optimizer.apply_gradients([(gd+gr,v) for gd, gr, v in zip(gradients_dist, gradients_reg, trained_variables) if gd is not None] )
        train_loss(distillation_loss)
    return training, train_loss


class learning_rate_scheduler(tf.keras.layers.Layer):
    def __init__(self, init_lr, total_epoch, decay_points, decay_rate):
        super(learning_rate_scheduler, self).__init__()
        self.init_lr = init_lr
        self.total_epoch = total_epoch
        self.decay_points = decay_points
        self.decay_rate = decay_rate
        self.current_lr = init_lr
        
    def call(self, epoch):
        with tf.name_scope('learning_rate_scheduler'):
            Learning_rate = self.init_lr
            for i, dp in enumerate(self.decay_points):
                Learning_rate = tf.cond(tf.greater_equal(epoch, int(self.total_epoch*dp)), lambda : Learning_rate*self.decay_rate,
                                                                                           lambda : Learning_rate)
            self.current_lr = Learning_rate
            return Learning_rate
            
            
