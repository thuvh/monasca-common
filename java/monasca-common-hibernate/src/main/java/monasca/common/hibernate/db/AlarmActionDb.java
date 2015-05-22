/*
 * Copyright 2015 FUJITSU LIMITED
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License
 * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the License for the specific language governing permissions and limitations under
 * the License.
 */
package monasca.common.hibernate.db;

import java.io.Serializable;

import javax.persistence.EmbeddedId;
import javax.persistence.Entity;
import javax.persistence.Table;

import monasca.common.model.alarm.AlarmState;

@Entity
@Table(name = "alarm_action")
public class AlarmActionDb implements Serializable {

  @EmbeddedId
  private AlarmActionId alarmActionId;

  public AlarmActionDb() {
    this("", AlarmState.UNDETERMINED, "");
  }

  public AlarmActionDb(String alarm_definition_id, AlarmState alarm_state, String action_id) {
    super();
    this.alarmActionId = new AlarmActionId(alarm_definition_id, alarm_state, action_id);
  }

  public AlarmActionId getAlarmActionId() {
    return alarmActionId;
  }

  public void setAlarmActionId(AlarmActionId alarmActionId) {
    this.alarmActionId = alarmActionId;
  }
}
